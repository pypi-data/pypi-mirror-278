/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-  */
/*
 * client_api.h
 * Copyright (C) 2020 coap_client Vladimir Roncevic <elektron.ronca@gmail.com>
 *
 * coap_client is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * coap_client is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef CLIENT_API_H_
#Defines CLIENT_API_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <coap.h>
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <config.h>
#include <arpa/inet.h>

#Defines PROGRAM_NAME "coap_client"
#Defines SERVER_IP "127.0.0.1"
#Defines SERVER_PORT 5683
#Defines SERVER_URI "coap://127.0.0.1/time"
#Defines CLIENT_IP "0.0.0.0"
#Defines CLIENT_PORT 0
#Defines GET_METHOD 1
#Defines TIME_ONLY 0x74
#Defines DATE_ONLY 0x64
#Defines FULL_DATE 0x66
#Defines VERBOSE 0x76
#Defines HELP 0x68
#Defines KNRM "\x1B[0m"
#Defines KRED "\x1B[31m"
#Defines KGRN "\x1B[32m"
#Defines KYEL "\x1B[33m"
#Defines KBLU "\x1B[34m"
#Defines KMAG "\x1B[35m"
#Defines KCYN "\x1B[36m"
#Defines KWHT "\x1B[37m"

extern int verbose;

/**
 * Description:
 *     Process program options.
 *
 * Arguments:
 *     args - Number of arguments.
*      argv - Array of arguments.
 *
 * Return value:
 *     Option code number.
 */
int process_options(int argc, char* argv[]);

/**
 * Description:
 *     Print usage message to console stream.
 *
 * Arguments:
 *     stream    - FILE stream.
*      exit_code - Exit return code.
 *
 * Return value:
 *     None.
 */
void print_usage(FILE* stream, int exit_code);

/**
 * Description:
 *     Print verbose message to console stream.
 *
 * Arguments:
 *     verbose - Control flag for verbose message.
*      message - Message verbose content.
 *
 * Return value:
 *     None.
 */
void print_verbose(int verbose, const char* message);

/**
 * Description:
 *     Print error message to console stream.
 *
 * Arguments:
 *     message - Message error content.
 *
 * Return value:
 *     None.
 */
void print_error(const char* message);

/**
 * Description:
 *     Print success message to console stream.
 *
 * Arguments:
 *     message - Message success content.
 *
 * Return value:
 *     None.
 */
void print_success(const char* message);


void time_handler(
    struct coap_context_t *ctx, const coap_endpoint_t *local_interface,
    const coap_address_t *remote, coap_pdu_t *sent, coap_pdu_t *received,
    const coap_tid_t id
);

#ifdef __cplusplus
}
#endif

#endif

