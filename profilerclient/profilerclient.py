#!/usr/bin/env python
#
# Client to launch profiling requests to djangoshop instance, part of Django
# Profiling probe of concept project.
#
#

import random
import csv
import json
import Queue
from threading import Thread
import os.path

from vendor.BasicBenchmarker import BasicBenchmarker
from vendor.Requester import Requester

# Codes

EXIT_NO_LOADING_PAGE_RESPONSE = -4040
EXIT_NO_BUY_PAGE_RESPONSE = -4041
EXIT_EMPTY_OUTPUT_QUEUE = -8000
EXIT_CSV = -9000
EXIT_SUCCESS = 0

HTTP_ERROR_UNKNOWN = -100

# Profiler Configuration

DEBUG_MODE = True
USER_AGENT = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.0"


# Djangoshop constants

APP_RDBMS_DIRNAME = 'rdbms'
APP_CASSANDRA_DIRNAME = 'cassandra'

# Fields got after profiling requests

RESULT_FIELDS = [

    # Benchmark

    'concurrent_requests',
    'benchmark_title',

    # Opening

    'client_home_elapsed_seconds',
    'client_home_error_msg',
    'client_home_http_code',
    'client_home_result',
    'client_home_started_time',
    'client_home_stopped_time',

    # Purchasing server results

    'server_buy_cpu_usage',
    'server_buy_memory_usage',
    'server_buy_elapsed_seconds',
    'server_buy_error_msg',
    'server_buy_result',
    'server_buy_started_time',
    'server_buy_stopped_time',

    # Purchasing client results

    'client_buy_elapsed_seconds',
    'client_buy_error_msg',
    'client_buy_http_code',
    'client_buy_result',
    'client_buy_started_time',
    'client_buy_stopped_time',
]


# Helper Functions

def rand_email(name_length=10):
    """
    Returns an email address of a valid domain.
    :return:
    """
    characters = '0123456789abcdefghijklmnopqrstvwyz'

    email = ''.join(random.choice(characters) for i in range(name_length))
    email += '@hotmail.com'

    return email


def rand_product_id(app):
    """
    Returns an id randomly
    :param app: string
    :return: int|string
    """
    if app == APP_RDBMS_DIRNAME:
        valid_products = [2, 3, 4, 5]

    elif app == APP_CASSANDRA_DIRNAME:
        valid_products = [
            'c382310f-bbf9-445b-bec8-cfb9d723cda7',
            '734951a1-b6b4-4412-af22-791366fe8698',
            'f259a3b5-e8bd-4494-b6ac-d1bd269c88a2',
            '466a83c1-f2c2-4e35-8d10-8533f496a8e2',
            '04a96d73-3aa3-4ee7-b52e-b44351805b95',
        ]
    returner = random.choice(seq=valid_products)

    return returner


def rand_quantity(maximum=99):
    """
    Returns quantity value randomly
    :param maximum: int
    :return: int
    """
    returner = random.randrange(1, maximum)

    return returner


def homepage_response(target):
    """
    Request the purchasing form and returns the content of response
    :param target: string url
    :return HttpResponse
    """
    try:

        response = Requester.open_request(request=target)

    except Exception, e:
        raise

    return response


def homepage_results(report, error_msg, http_code):
    """
    Returns a dict with the homepage result fields
    :param report: dict report after homepage request
    :param error_msg: string any error
    :param http_code: response code
    :return: dict
    """

    results = {}

    if http_code == 200 and not error_msg:
        result = True

    else:
        result = False

    try:
        results['client_home_elapsed_seconds'] = report['elapsed_seconds']
        results['client_home_started_time'] = report['started_time']
        results['client_home_stopped_time'] = report['stopped_time']
        results['client_home_http_code'] = http_code
        results['client_home_result'] = result

    except IndexError, e:
        error_msg = append_error(error_msg,
                                 'Request report is missing. Exception: {!s}'
                                 .format(e.message))
        results['client_home_result'] = False

    except Exception, e:
        error_msg = append_error(error_msg, e.message)
        results['client_home_result'] = False

    results['client_home_error_msg'] = error_msg

    return results


def purchase_response(target, product_id, form_fields):
    """
    Request the purchasing form and returns the content of response
    :param target: string url
    :param form_fields: dict
    :return HttpResponse
    """
    try:

        purchase_url = target.format(product_id)

        response = Requester.open_request(request=purchase_url,
                                          post_fields=form_fields)

    except Exception:
        raise

    return response


def purchase_results(report, content, error_msg, http_code):
    """
    Returns a dict with the purchase result fields.

    The error message built in this function is exclusively the client error
    message. Server error message always is coming from server only.

    :param report: dict report after homepage request
    :param content: string response content
    :param error_msg: string any error
    :param http_code: response code
    :return: dict
    """

    results = {}

    if http_code == 200 and not error_msg:
        result = True

    else:
        result = False

    # server

    try:
        results['server_buy_elapsed_seconds'] = content['elapsed_seconds']
        results['server_buy_started_time'] = content['started_time']
        results['server_buy_stopped_time'] = content['stopped_time']
        results['server_buy_cpu_usage'] = content['cpu_usage']
        results['server_buy_memory_usage'] = content['memory_usage']
        results['server_buy_result'] = content['result']

        error_msg = append_error(error_msg, content['error_msg'])

    except IndexError, e:
        error_msg = append_error(error_msg,
                                 'Server report is missing. Exception: {!s}' \
                                 .format(e.message))
        results['client_buy_result'] = False

    except Exception, e:
        error_msg = append_error(error_msg, e.message)
        results['client_buy_result'] = False

    results['server_buy_error_msg'] = error_msg

    # client

    try:
        results['client_buy_elapsed_seconds'] = report['elapsed_seconds']
        results['client_buy_started_time'] = report['started_time']
        results['client_buy_stopped_time'] = report['stopped_time']
        results['client_buy_http_code'] = http_code
        results['client_buy_result'] = result

    except IndexError, e:
        error_msg = append_error(error_msg,
                                 'Request report is missing. Exception: {!s}'
                                 .format(e.message))
        results['client_buy_result'] = False

    except Exception, e:
        error_msg = append_error(error_msg, e.message)
        results['client_buy_result'] = False

    results['client_buy_error_msg'] = error_msg

    return results


def response_report(content):
    """
    Converts json content of the response to key pairs and returns them
    :param content: string json formatted
    :return: dict
    """
    try:
        report = json.loads(content)

    except TypeError:
        raise

    except ValueError:
        raise

    return report


def append_error(error_msg, new):
    """
    Append error message.
    :param error_msg: string
    :param new: string
    :return: string
    """
    if error_msg:
        error_msg += ' + '
        error_msg += new
        
    else:
        error_msg = new

    return error_msg


def print_debug(message):
    """
    Prints debug messages if debug mode is enabled
    :param message:
    :return:
    """
    if DEBUG_MODE:
        message = '[' + BasicBenchmarker.now() + '] ' + message
        print(message)

    pass


def write_results(filepath, field_names, rows):
    """
    Writes results of profiling in a csv file row.
    :param filepath: string
    :param field_names: restricted field names
    :param rows: list<dict>
    :return: boolean
    """
    file_exists = os.path.isfile(filepath)

    with open(filepath, 'ab') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names,
                                    extrasaction='ignore', delimiter=';', 
                                    quoting=csv.QUOTE_NONNUMERIC)

        if not file_exists:
            csv_writer.writeheader()

        for row in rows:
            csv_writer.writerow(row)

    return True


def print_header():
    """
    Prints module header
    """
    if DEBUG_MODE:
        print
        print '   ____      _   _    _   _  ____  ___    \n'\
              '  |  _ \\    | | / \\  | \\ | |/ ___|/ _ \\   \n'\
              '  | | | |_  | |/ _ \\ |  \\| | |  _| | | |  \n'\
              '  | |_| | |_| / ___ \\| |\\  | |_| | |_| |  \n'\
              '  |____/_\\___/_/__ \\_\\_|_\\_|\\____|\\___/__ \n'\
              ' |  _ \\|  _ \\ / _ \\|  ___|_ _| |   | ____|\n'\
              ' | |_) | |_) | | | | |_   | || |   |  _|  \n'\
              ' |  __/|  _ <| |_| |  _|  | || |___| |___ \n'\
              ' |_|   |_| \\_\\\\___/|_|   |___|_____|_____|\n'\

    pass


def benchmark(rows, product_id, quantity, email, homepage_url,
              purchase_url):
    """
    Consume the benchmarking requests and process the responses.
    Appends a row in the rows Queue.
    This function is managed by multiples threads at the same time, for this
    reason the Queue rows is being updated asynchronously by all consuming
    threads.
    :param rows: Queue
    :param product_id: int
    :param quantity: int
    :param email: string
    :param homepage_url: string
    :param purchase_url: string
    """
    row = {}
    response_content = ''
    error_msg = ''

    benchmarker = BasicBenchmarker(usage=False)

    purchase_fields = {'email': email, 'repeat_email': email,
                       'quantity': quantity}

    #
    # opens homepage
    #

    benchmarker.start()

    try:
        response = homepage_response(homepage_url)

        response_code = response.code

        print_debug('Opened page for loading test')

    except Exception, e:
        error_msg = append_error(error_msg, e.message)

        response_code = HTTP_ERROR_UNKNOWN

        print_debug('Error loading page test {page}. Exception: {exception}'
                    .format(page=homepage_url, exception=e.message))

        #exit(EXIT_NO_LOADING_PAGE_RESPONSE)

    client_report = benchmarker.report()   # initializes client report

    new_row_fields = homepage_results(report=client_report,
                                      error_msg=error_msg,
                                      http_code=response_code)

    row.update(new_row_fields)

    error_msg = ''		# resets error message

    #
    # purchase
    #

    benchmarker.start()

    try:
        response = purchase_response(target=purchase_url,
                                     product_id=product_id,
                                     form_fields=purchase_fields)

        response_content = Requester.read_response(response)

        response_code = response.code

        print_debug('Purchase is done')

    except Exception, e:
        error_msg = append_error(error_msg, e.message)

        response_code = HTTP_ERROR_UNKNOWN

        print_debug('Error purchasing on "{page}". Exception: {exception}'
                    .format(page=purchase_url, exception=e.message))

        #exit(EXIT_NO_BUY_PAGE_RESPONSE)

    benchmarker.stop()

    client_report = benchmarker.report()   # initializes client report

    try:
        server_report = response_report(response_content)

        print_debug('Server report is analysed')

    except Exception, e:
        server_report = {}

        error_msg = append_error(error_msg, e.message)

        print_debug('Error analysing report for content "{content}".'
                    ' Exception: {exception}'
                    .format(content=response_content, exception=e.message))

    new_row_fields = purchase_results(report=client_report,
                                      content=server_report,
                                      error_msg=error_msg,
                                      http_code=response_code)

    row.update(new_row_fields)

    rows.put(row)

    pass


# Main

def run(concurrent, host, app, buy_query, output_file, home_query='',
        benchmark_title=''):
    """
    Main handler of this module.
    :return: boolean
    """
    print_header()
    print_debug('Started profiling for:\n'
                '\thost: {host}\n'
                '\tloading page query: {home_query}\n'
                '\tbuy query: {buy_query}\n'
                '\toutput file: {output_file}'.format(host=host,
                                                      home_query=home_query,
                                                      buy_query=buy_query,
                                                      output_file=output_file))

    results = Queue.Queue(maxsize=concurrent)

    host = host + '/' + app
    homepage_url = host + home_query
    purchase_url = host + buy_query

    threads = []

    counter = concurrent

    # start threads

    while counter > 0:

        product_id = rand_product_id(app)
        quantity = rand_quantity()
        email = rand_email()

        thread_params = {'rows': results, 'product_id': product_id,
                         'quantity': quantity, 'email': email,
                         'homepage_url': homepage_url,
                         'purchase_url': purchase_url}

        thread = Thread(target=benchmark, kwargs=thread_params)

        thread.start()

        threads.append(thread)

        counter -= 1  # discount

        print_debug('New benchmark thread is started.')

    # wait the threads finish

    counter = len(threads)

    if concurrent != counter:

        print_debug('WARNING: Check why there are not the same configured'
                    'concurrent value ({!s}) as created threads ({!s}).'
                    .format(concurrent, counter))

    for thread in threads:

        thread.join()

        counter -= 1  # discount

        print_debug('Benchmark thread is finished the job.')

        print_debug('Remaining {!s} thread/s.'
                    .format(counter))

    # Write rows in file

    if results.empty():

        print_debug('Rows queue is empty.')

        exit(EXIT_EMPTY_OUTPUT_QUEUE)

    try:

        file_exists = os.path.isfile(output_file)

        with open(output_file, 'ab') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=RESULT_FIELDS,
                                        extrasaction='ignore', delimiter=';',
                                        quoting=csv.QUOTE_NONNUMERIC)

            if not file_exists:
                csv_writer.writeheader()

            while not results.empty():

                row = results.get()

                row['concurrent_requests'] = concurrent
                row['benchmark_title'] = benchmark_title

                csv_writer.writerow(row)

        print_debug('Output file "{file}" is written'.format(file=output_file))

    except csv.Error, e:
        print_debug('Error writing on output file "{file}".'
                    ' Exception: {exception}'.format(file=output_file,
                                                     exception=e.message))

        exit(EXIT_CSV)

    pass


# Entry point

if __name__ == '__main__':
    import argparse

    # Get arguments

    parser = argparse.ArgumentParser(description='Client to launch profiling'
                                                 ' requests to djangoshop'
                                                 ' instance.\n Part of django'
                                                 ' profiling probes'
                                                 ' environment.')

    parser.add_argument('-a', '--benchmark_title', help='Benchmark title',
                        default='')

    parser.add_argument('-c', '--concurrent', help='Concurrent factor.',
                        default=1, type=int)

    parser.add_argument('-t', '--target',
                        help='Target domain. No slash at end.', required=True)

    parser.add_argument('-d', '--app_dirname',
                        help='Directory name of the Django App.', required=True)

    parser.add_argument('-p', '--page_query', help='Loading page URI query',
                        default='')

    parser.add_argument('-b', '--buy_query', help='Purchasing URI query',
                        default='/{!s}/purchase/1/')

    parser.add_argument('-o', '--output', help='Output csv file path',
                        default='report.csv')

    args = parser.parse_args()

    run(concurrent=args.concurrent, host=args.target, app=args.app_dirname,
        home_query=args.page_query, buy_query=args.buy_query,
        output_file=args.output)

    exit(EXIT_SUCCESS)
