#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Definition of region-specific functions
"""

from itaqa.crawler import piemonte, lombardia

REGION_CRAWLERS = {'lombardia': lombardia.get_AQS_list}
