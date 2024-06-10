/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-  */
/*
 * server_api.h
 * Copyright (C) 2020 coap_server Vladimir Roncevic <elektron.ronca@gmail.com>
 *
 * coap_server is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * coap_server is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef SERVER_API_H_
#Defines SERVER_API_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <time.h>
#include <coap.h>
#include <config.h>

/**
 * Description:
 *     Getting current local time on host.
 *
 * Arguments:
 *     None
 *
 * Return value:
 *     Current local time from host in string format | NULL.
 */
char* get_time(void);

/**
 * Description:
 *     Converting integer value to BCD code.
 *
 * Arguments:
 *     integer_value - integer value
 *
 * Return value:
 *     BCD code after conversion from integer value
 */
void time_handler(
    coap_context_t *ctx, struct coap_resource_t *resource,
    const coap_endpoint_t *local_interface, coap_address_t *peer,
    coap_pdu_t *request, str *token, coap_pdu_t *response
);

#ifdef __cplusplus
}
#endif

#endif

