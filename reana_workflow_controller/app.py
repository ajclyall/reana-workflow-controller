# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017 CERN.
#
# REANA is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# REANA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# REANA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.

"""REANA Workflow Controller Instance."""

import threading

from flask import current_app

from reana_workflow_controller.factory import create_app
from reana_workflow_controller.tasks import consume_job_queue


class JobQueueConsumer(object):
    """Job queue consumer class.

    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self):
        """Initialize JobQueueConsumer."""
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()        # Start the execution

    def run(self):
        """Run forever."""
        while True:
            consume_job_queue()


job_queue_consumer = JobQueueConsumer()

app = create_app()


@app.teardown_appcontext
def shutdown_session(response_or_exc):
    """Close session on app teardown."""
    current_app.session.remove()
    return response_or_exc
