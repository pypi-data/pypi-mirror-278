/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-  */
/*
 * process_options.c
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

#include "client_api.h"

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
int process_options(int argc, char* argv[]) {
    int option = -1;
    const char* const short_options = "tdf:vh";
    struct option long_options[] = {
        {"time", 0, NULL, 't'},
        {"date", 0, NULL, 'd'},
        {"full", 0, NULL, 'f'},
        {"verbose", 0, NULL, 'v'},
        {"help", 0, NULL, 'h'},
        {NULL, 0, NULL, 0}
    };
    option = getopt_long(argc, argv, short_options, long_options, NULL);
    return option;
}

