# -*- coding: utf-8 -*-

'''
torstack.handler.rest
rest handler definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

from __future__ import absolute_import, unicode_literals

import sys
import json
import tornado.web

class RestHandler(tornado.web.RequestHandler):

    def initialize(self):
        self._token_id = None
        self._token_data = None
        self.db = self.settings['_storage_mysql']
        self.redis = self.settings['_storage_redis']

        self.token = self.settings['token']
        self.set_header('Content-Type', 'text/json')
        if self.settings['rest_config']['allow_remote_access']:
            self.access_control_allow()

    def access_control_allow(self):
        # 允许 JS 跨域调用
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Depth, User-Agent, X-File-Size, "
                                                        "X-Requested-With, X-Requested-By, If-Modified-Since, "
                                                        "X-File-Name, Cache-Control, Token")
        self.set_header('Access-Control-Allow-Origin', '*')

    def get(self):
        """ Executes get method """
        self._exe('GET')

    def post(self):
        """ Executes post method """
        self._exe('POST')

    def put(self):
        """ Executes put method """
        self._exe('PUT')

    def patch(self):
        """ Executes patch method """
        self._exe('PATCH')

    def delete(self):
        """ Executes put method """
        self._exe('DELETE')

    def _exe(self, method):
        """ Executes the python function for the Rest Service """
        request_path = self.request.path
        path = request_path.split('/')
        services_and_params = list(filter(lambda x: x != '', path))
        content_type = None
        if 'Content-Type' in self.request.headers.keys():
            content_type = self.request.headers['Content-Type']

        # Get all funcion names configured in the class RestHandler
        functions = list(filter(lambda op: hasattr(getattr(self, op), '_service_name') == True and inspect.ismethod(
            getattr(self, op)) == True, dir(self)))
        # Get all http methods configured in the class RestHandler
        http_methods = list(map(lambda op: getattr(getattr(self, op), '_method'), functions))

        if method not in http_methods:
            raise tornado.web.HTTPError(405, 'The service not have %s verb' % method)
        for operation in list(map(lambda op: getattr(self, op), functions)):
            service_name = getattr(operation, '_service_name')
            service_params = getattr(operation, '_service_params')
            # If the _types is not specified, assumes str types for the params
            params_types = getattr(operation, "_types") or [str] * len(service_params)
            params_types = params_types + [str] * (len(service_params) - len(params_types))
            produces = getattr(operation, '_produces')
            consumes = getattr(operation, '_consumes')
            services_from_request = list(filter(lambda x: x in path, service_name))
            query_params = getattr(operation, '_query_params')
            manual_response = getattr(operation, '_manual_response')
            catch_fire = getattr(operation, '_catch_fire')

            if operation._method == self.request.method and service_name == services_from_request and len(
                    service_params) + len(service_name) == len(services_and_params):
                try:
                    params_values = self._find_params_value_of_url(service_name,
                                                                   request_path) + self._find_params_value_of_arguments(
                        operation)
                    p_values = self._convert_params_values(params_values, params_types)
                    if consumes == None and produces == None:
                        consumes = content_type
                        produces = content_type
                    if consumes == mediatypes.APPLICATION_XML:
                        if params_types[0] in [str]:
                            param_obj = xml.dom.minidom.parseString(self.request.body)
                        else:
                            param_obj = convertXML2OBJ(params_types[0],
                                                       xml.dom.minidom.parseString(self.request.body).documentElement)
                        p_values.append(param_obj)
                    elif consumes == mediatypes.APPLICATION_JSON:
                        body = self.request.body
                        if sys.version_info > (3,):
                            body = str(self.request.body, 'utf-8')
                        if params_types[0] in [dict, str]:
                            param_obj = json.loads(body)
                        else:
                            param_obj = convertJSON2OBJ(params_types[0], json.loads(body))
                        p_values.append(param_obj)
                    response = operation(*p_values)

                    if response == None:
                        return

                    if produces:
                        self.set_header('Content-Type', produces)

                    if manual_response:
                        return

                    if produces == mediatypes.APPLICATION_JSON and hasattr(response, '__module__'):
                        response = convert2JSON(response)
                    elif produces == mediatypes.APPLICATION_XML and hasattr(response, '__module__') and not isinstance(
                            response, xml.dom.minidom.Document):
                        response = convert2XML(response)

                    if produces == mediatypes.APPLICATION_JSON and isinstance(response, dict):
                        self.write(response)
                        self.finish()
                    elif produces == mediatypes.APPLICATION_JSON and isinstance(response, list):
                        self.write(json.dumps(response))
                        self.finish()
                    elif produces in [mediatypes.APPLICATION_XML, mediatypes.TEXT_XML] and isinstance(response,
                                                                                                      xml.dom.minidom.Document):
                        self.write(response.toxml())
                        self.finish()
                    else:
                        self.gen_http_error(500, 'Internal Server Error : response is not %s document' % produces)
                        if catch_fire == True:
                            raise PyRestfulException('Internal Server Error : response is not %s document' % produces)
                except Exception as detail:
                    self.gen_http_error(500, 'Internal Server Error : %s' % detail)
                    if catch_fire == True:
                        raise PyRestfulException(detail)

    def _find_params_value_of_url(self, services, url):
        """ Find the values of path params """
        values_of_query = list()
        i = 0
        url_split = url.split('/')
        values = [item for item in url_split if item not in services and item != '']
        for v in values:
            if v != None:
                values_of_query.append(v)
                i += 1
        return values_of_query

    def _find_params_value_of_arguments(self, operation):
        values = []
        if len(self.request.arguments) > 0:
            a = operation._service_params
            b = operation._func_params
            params = [item for item in b if item not in a]
            for p in params:
                if p in self.request.arguments.keys():
                    v = self.request.arguments[p]
                    values.append(v[0])
                else:
                    values.append(None)
        elif len(self.request.arguments) == 0 and len(operation._query_params) > 0:
            values = [None] * (len(operation._func_params) - len(operation._service_params))
        return values

    def _convert_params_values(self, values_list, params_types):
        """ Converts the values to the specifics types """
        values = list()
        i = 0
        for v in values_list:
            if v != None:
                values.append(types.convert(v, params_types[i]))
            else:
                values.append(v)
            i += 1
        return values

    def gen_http_error(self, status, msg):
        """ Generates the custom HTTP error """
        self.clear()
        self.set_status(status)
        self.write('<html><body>' + str(msg) + '</body></html>')
        self.finish()

    @classmethod
    def get_services(self):
        """ Generates the resources (uri) to deploy the Rest Services """
        services = []
        for f in dir(self):
            o = getattr(self, f)
            if callable(o) and hasattr(o, '_service_name'):
                services.append(getattr(o, '_service_name'))
        return services

    @classmethod
    def get_paths(self):
        """ Generates the resources from path (uri) to deploy the Rest Services """
        paths = []
        for f in dir(self):
            o = getattr(self, f)
            if callable(o) and hasattr(o, '_path'):
                paths.append(getattr(o, '_path'))
        return paths

    @classmethod
    def get_handlers(self):
        """ Gets a list with (path, handler) """
        svs = []
        paths = self.get_paths()
        for p in paths:
            s = re.sub(r'(?<={)\w+}', '.*', p).replace('{', '')
            o = re.sub(r'(?<=<)\w+', '', s).replace('<', '').replace('>', '').replace('&', '').replace('?', '')
            svs.append((o, self))

        return svs

