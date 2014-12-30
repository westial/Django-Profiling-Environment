#!/usr/bin/env python
#
# Client to launch profiling requests to djangoshop instance, part of Django
# Profiling probe of concept project.
#
# How it works:
#
# It's a loop running as times as set in parameter and gets profiling data
# each turn. The repeated action does actions described below and gets timing
# and performance reports, got from server side and also from client side:
#
# a) Opens homepage. Reports times recorded from client side:
#
#       1. client_home_elapsed_seconds: elapsed seconds between started request
#          and response is received.
#       2. client_home_error_msg: error message if exists.
#       3. client_home_http_code: response http code.
#       4. client_home_result: boolean considering result satisfaction.
#       5. client_home_started_time: request starting time stamp.
#       6. client_home_stopped_time: received response time stamp.
#
# b) Purchase on main server. Reports times and performance report on server
#    side:
#
#       1. server_buy_cpu_usage: cpu usage percentage in server.
#       2. server_buy_elapsed_seconds: elapsed seconds between received request
#          and saved database records of purchase.
#       3. server_buy_error_msg: error message if exists.
#       4. server_buy_memory_usage: memory usage megabytes in server.
#       5. server_buy_result: boolean considering result satisfaction.
#       6. server_buy_started_time: received request time stamp.
#       7. server_buy_stopped_time: saved records time stamp.
#
# c) Purchase on second server. Reports times and performance report on server
#    side for server which optionally hosts the external webservices:
#
#       1. server_rest_cpu_usage: cpu usage percentage in server.
#       2. server_rest_elapsed_seconds: elapsed seconds between received request
#          and saved database records of purchase.
#       3. server_rest_error_msg: error message if exists.
#       4. server_rest_memory_usage: memory usage megabytes in server.
#       5. server_rest_result: boolean considering result satisfaction.
#       6. server_rest_started_time: received request time stamp.
#       7. server_rest_stopped_time: saved records time stamp.
#
# d) Purchase on client. Reports times report from client side:
#
#       1. client_buy_elapsed_seconds: elapsed seconds between started request
#          and response is received.
#       2. client_buy_error_msg: error message if exists.
#       3. client_buy_http_code: response http code.
#       4. client_buy_result: boolean considering result satisfaction.
#       5. client_buy_started_time: request starting time stamp.
#       6. client_buy_stopped_time: received response time stamp.
#

import random
import csv
import json

from vendor.BasicBenchmarker import BasicBenchmarker
from vendor.Requester import Requester

# Exit codes

EXIT_CSV = -9000
EXIT_NO_LOADING_PAGE_RESPONSE = -4040
EXIT_NO_BUY_PAGE_RESPONSE = -4041

# Profiler Configuration

DEBUG_MODE = True
USER_AGENT = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.0"


# Fields got after profiling requests

RESULT_FIELDS = [

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


def rand_product_id():
    """
    Returns an id randomly
    :return: int
    """
    valid_products = [2, 3, 4, 5]
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

    with open(filepath, 'wb') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names,
                                    extrasaction='ignore', delimiter=';', 
                                    quoting=csv.QUOTE_NONNUMERIC)

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


# Main

def profiling(loops, host, buy_query, output_file, home_query=''):
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

    rows = []
    homepage_url = host + home_query
    purchase_url = host + buy_query

    profiler = BasicBenchmarker(usage=False)

    while loops > 0:

        product_id = rand_product_id()
        quantity = rand_quantity()
        email = rand_email()

        row = {}
        response = None
        response_content = ''
        error_msg = ''

        purchase_fields = {'email': email, 'repeat_email': email,
                           'quantity': quantity}

        #
        # opens homepage
        #

        profiler.start()

        try:
            response = homepage_response(homepage_url)

            print_debug('Opened page for loading test')

        except Exception, e:
            # error_msg = append_error(error_msg, e.message)

            print_debug('Error loading page test {page}. Exception: {exception}'
                        .format(page=homepage_url, exception=e.message))

            exit(EXIT_NO_LOADING_PAGE_RESPONSE)

        client_report = profiler.report()   # initializes client report

        new_row_fields = homepage_results(report=client_report,
                                          error_msg=error_msg,
                                          http_code=response.code)

        row.update(new_row_fields)

        error_msg = ''		# resets error message

        #
        # purchase
        #

        profiler.start()

        try:
            response = purchase_response(target=purchase_url,
                                         product_id=product_id,
                                         form_fields=purchase_fields)

            response_content = Requester.read_response(response)

            print_debug('Purchase is done')

        except Exception, e:
            # error_msg = append_error(error_msg, e.message)

            print_debug('Error purchasing on "{page}". Exception: {exception}'
                        .format(page=purchase_url, exception=e.message))

            exit(EXIT_NO_BUY_PAGE_RESPONSE)

        client_report = profiler.report()   # initializes client report

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
                                          http_code=response.code)

        row.update(new_row_fields)

        rows.append(row)

        loops -= 1  # discount

        print_debug('Row is appended to results report.')

        print_debug('Remains {loops} request/s.'
                    .format(loops=loops))

    try:
        write_results(output_file, RESULT_FIELDS, rows)

        print_debug('Output file "{file}" is written'.format(file=output_file))

    except csv.Error, e:
        print_debug('Error writing on output file "{file}".'
                    ' Exception: {exception}'.format(file=output_file,
                                                     exception=e.message))

        exit(EXIT_CSV)


# commandline entry

if __name__ == '__main__':
    import argparse

    # Get arguments

    parser = argparse.ArgumentParser(description='Client to launch profiling'
                                                 ' requests to djangoshop'
                                                 ' instance.\n Part of django'
                                                 ' profiling probes'
                                                 ' environment.')

    parser.add_argument('-r', '--repeat', help='Repeat factor.', default=1,
                        type=int)

    parser.add_argument('-t', '--target', help='Root url of the target.',
                        required=True)

    parser.add_argument('-p', '--page_query', help='Loading page URI query',
                        default='')

    parser.add_argument('-b', '--buy_query', help='Purchasing URI query',
                        default='/{!s}/purchase/1/')

    parser.add_argument('-o', '--output', help='Output csv file path',
                        default='report.csv')

    args = parser.parse_args()

    profiling(loops=args.repeat, host=args.target, home_query=args.page_query,
              buy_query=args.buy_query, output_file=args.output)
