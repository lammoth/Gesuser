#!/usr/bin/env python
# -*- coding: utf-8 -*-

ALL_DOCS = '''
function (doc) {
    emit(null, doc);
}
'''

SPEC_DOC = '''
function (doc) {
    if (%s == "%s") {
        emit(null, doc);   
    }
}
'''