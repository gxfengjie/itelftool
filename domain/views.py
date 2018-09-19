#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
from django.core.urlresolvers import reverse
from accounts.permission import permission_verify
from domain.models import DomainRrecord
from domain.domain import get_domain_info


# 用户列表展示功能
@login_required()
@permission_verify()
def domain_list(request):
    all_domain = DomainRrecord.objects.all()
    results = {
        'all_domain':  all_domain,
    }
    return render(request, 'domain/domain_list.html', results)


@login_required
@permission_verify()
def domain_add(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        name = request.POST.get('name')
        domain_info = get_domain_info(comment,name)[0]
        DomainRrecord.objects.create(comment=domain_info['comment'],name=domain_info['name'],ctime=domain_info['ctime'],etime=domain_info['etime'],ip=domain_info['ip'],ip_source=domain_info['ip_source'],domain_record_num=domain_info['domain_record_num'],domain_nature=domain_info['domain_nature'],domain_company=domain_info['domain_company'])
        return HttpResponseRedirect(reverse('domain_list'))
    else:
        pass
    results = {
        'request': request,
    }
    return render(request, 'domain/domain_add.html', results)


@login_required
@permission_verify()
def domain_del(request, id):
    DomainRrecord.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('domain_list'))



@login_required
@permission_verify()
def domain_update(request, id):
    domain_info = DomainRrecord.objects.get(id=id)
    comment = domain_info.comment
    name = domain_info.name
    domain_info = get_domain_info(comment,name)[0]
    DomainRrecord.objects.filter(id=id).update(comment=domain_info['comment'],name=domain_info['name'],ctime=domain_info['ctime'],etime=domain_info['etime'],ip=domain_info['ip'],ip_source=domain_info['ip_source'],domain_record_num=domain_info['domain_record_num'],domain_nature=domain_info['domain_nature'],domain_company=domain_info['domain_company'])
    return HttpResponseRedirect(reverse('domain_list'))



@login_required
@permission_verify()
def domain_search_input(request):
    return render(request, 'domain/domain_search.html')


@login_required
@permission_verify()
def domain_search_result(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        name = request.POST.get('name')
        domain_info = get_domain_info(comment,name)[0]
        
        results = {
            'request': request,
            'comment':domain_info['comment'],
            'name':domain_info['name'],
            'ctime':domain_info['ctime'],
            'etime':domain_info['etime'],
            'ip':domain_info['ip'],
            'ip_source':domain_info['ip_source'],
            'domain_record_num':domain_info['domain_record_num'],
            'domain_nature':domain_info['domain_nature'],
            'domain_company':domain_info['domain_company'],
                }
    else:
        return HttpResponse('Nothing to search!')
    return render(request, 'domain/domain_search_result.html', results)
