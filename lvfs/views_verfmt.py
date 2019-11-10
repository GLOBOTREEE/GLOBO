#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Richard Hughes <richard@hughsie.com>
#
# SPDX-License-Identifier: GPL-2.0+

from flask import request, url_for, redirect, flash, render_template
from flask_login import login_required

from lvfs import app, db

from .models import Verfmt
from .util import admin_login_required
from .util import _error_internal

@app.route('/lvfs/verfmt/all')
@login_required
@admin_login_required
def verfmt_all():
    verfmts = db.session.query(Verfmt).order_by(Verfmt.verfmt_id.asc()).all()
    return render_template('verfmt-list.html',
                           category='admin',
                           verfmts=verfmts)

@app.route('/lvfs/verfmt/add', methods=['POST'])
@login_required
@admin_login_required
def verfmt_add():
    # ensure has enough data
    if 'value' not in request.form:
        return _error_internal('No form data found!')
    value = request.form['value']
    if not value or value.find(' ') != -1:
        flash('Failed to add version format: Value needs to be valid', 'warning')
        return redirect(url_for('.verfmt_all'))

    # already exists
    if db.session.query(Verfmt).filter(Verfmt.value == value).first():
        flash('Failed to add version format: Already exists', 'info')
        return redirect(url_for('.verfmt_all'))

    # add verfmt
    verfmt = Verfmt(value=request.form['value'])
    db.session.add(verfmt)
    db.session.commit()
    flash('Added version format', 'info')
    return redirect(url_for('.verfmt_details', verfmt_id=verfmt.verfmt_id))

@app.route('/lvfs/verfmt/<int:verfmt_id>/delete')
@login_required
@admin_login_required
def verfmt_delete(verfmt_id):

    # get verfmt
    verfmt = db.session.query(Verfmt).\
            filter(Verfmt.verfmt_id == verfmt_id).first()
    if not verfmt:
        flash('No verfmt found', 'info')
        return redirect(url_for('.verfmt_all'))

    # delete
    db.session.delete(verfmt)
    db.session.commit()
    flash('Deleted version format', 'info')
    return redirect(url_for('.verfmt_all'))

@app.route('/lvfs/verfmt/<int:verfmt_id>/modify', methods=['POST'])
@login_required
@admin_login_required
def verfmt_modify(verfmt_id):

    # find verfmt
    verfmt = db.session.query(Verfmt).\
                filter(Verfmt.verfmt_id == verfmt_id).first()
    if not verfmt:
        flash('No version format found', 'info')
        return redirect(url_for('.verfmt_all'))

    # modify verfmt
    for key in ['name', 'example', 'value', 'fwupd_version']:
        if key in request.form:
            setattr(verfmt, key, request.form[key])
    db.session.commit()

    # success
    flash('Modified version format', 'info')
    return redirect(url_for('.verfmt_details', verfmt_id=verfmt_id))

@app.route('/lvfs/verfmt/<int:verfmt_id>/details')
@login_required
@admin_login_required
def verfmt_details(verfmt_id):

    # find verfmt
    verfmt = db.session.query(Verfmt).\
            filter(Verfmt.verfmt_id == verfmt_id).first()
    if not verfmt:
        flash('No version format found', 'info')
        return redirect(url_for('.verfmt_all'))

    # show details
    return render_template('verfmt-details.html',
                           category='admin',
                           verfmt=verfmt)