# Copyright 2012 Rackspace
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cliff.formatters.table import TableFormatter

__all__ = [
    'PaginatedListFormatter'
]


class PaginatedListFormatter(TableFormatter):
    def add_argument_group(self, parser):
        pass

    def emit_list(self, column_names, data, stdout, parsed_args):
        super(PaginatedListFormatter, self).emit_list(column_names, data,
                                                      stdout, parsed_args)

        returned_metadata = getattr(parsed_args, 'returned_metadata', {})
        limit = returned_metadata.get('limit', None)
        marker = returned_metadata.get('marker', None)
        next_marker = returned_metadata.get('next_marker', None)

        if len(data) >= 1 and limit:
            print ''
            print 'Displaying: %s' % (len(data))

        if limit:
            print 'Limit: %s' % (limit)

        if marker:
            print 'Marker in use: %s' % (marker)

        if next_marker:
            print 'Next marker: %s' % (next_marker)
