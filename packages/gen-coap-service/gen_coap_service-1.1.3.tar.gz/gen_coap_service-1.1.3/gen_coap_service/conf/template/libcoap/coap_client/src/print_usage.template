/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-  */
/*
 * print_usage.c
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
 *     Print usage message to console stream.
 *
 * Arguments:
 *     stream    - FILE stream.
*      exit_code - Exit return code.
 *
 * Return value:
 *     None.
 */
void print_usage(FILE* stream, int exit_code) {
#if Defines(__FreeBSD__)
    const char* program_name = getprogname();
#elif Defines(_GNU_SOURCE)
    const char* program_name = program_invocation_name;
#else
    const char* program_name = PROGRAM_NAME;
#endif
    fprintf(stream, "%s", KCYN);
    fprintf(stream, "Usage:  %s options\n", program_name);
    fprintf(stream,
        "  -t  --time     Get time info only\n"
        "  -d  --date     Get date info only\n"
        "  -f  --full     Get time and date info\n"
        "  -v  --verbose  Print verbose messages\n"
        "  -h  --help     Display this usage\n"
    );
    fprintf(stream,"%s", KNRM);
    exit(exit_code);
}

