# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from school.stjoseph.form import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from stjoseph.models import sjcuser
from stjoseph.models import presrqst
from stjoseph.models import schoolim
from django.core.mail import EmailMessage
from django.views.static import serve
from random import randint
from school import settings
import hashlib
import datetime
import Image
import os
import re
import urllib2

def home(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    return render_to_response('stjoseph/home.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def handle_404(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    errormsg = 'The page you requested does not exist! O_o'
    return render_to_response('stjoseph/404.html', {'uname':uname,'id':uid,'errormsg':errormsg,},
                               context_instance=RequestContext(request))

def handle_500(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    errormsg = 'An error occured while serving your request. Please report it to the Web Admin.'
    return render_to_response('stjoseph/404.html', {'uname':uname,'id':uid,'errormsg':errormsg,},
                               context_instance=RequestContext(request))

def printdata(request):
    raise Http404
    retdata = ""
    susers = sjcuser.objects.filter(act=True)
    for suser in susers:
        retdata += suser.email + ' , '
    return HttpResponse(retdata)

def uploadimage(request):
    raise Http404
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
        updone = False
        if str(uid) == str(1):  # change id
            schoolim.objects.all().delete()
            filelist = os.listdir(settings.MEDIA_ROOT+'/snaps')
            for imfile in filelist:
                if imfile[-4:] == '.jpg' or imfile[-4:] == '.JPG':
                    vtoall = True
                    if imfile[:1] == 'n':
                        vtoall = False
                    newpic = schoolim.objects.create(name=imfile, albname=str('random'), vistoall = vtoall) #change albname if required
                    #max_size = (800, 600)      #uncomment these to update pics
                    #t_size = (180, 135)
                    #im = Image.open(settings.MEDIA_ROOT+'/snaps/'+newpic.name)
                    #if im.size>max_size:
                    #    im.thumbnail(max_size)
                    #    im.save(str(settings.MEDIA_ROOT+'/snaps/'+newpic.name))
                    #if im.size>t_size:
                    #    im.thumbnail(t_size)
                    #    im.save(str(settings.MEDIA_ROOT+'/thumb/'+newpic.name))
            updone = True
            return render_to_response('stjoseph/uploadpic.html', {'uname':uname,'id':uid,'updone':updone,},
                               context_instance=RequestContext(request))
    raise Http404

def gallery(request,slow=0):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
        imobj = schoolim.objects.all()
    else:
        imobj = schoolim.objects.filter(vistoall=True)    
    return render_to_response('stjoseph/gallery.html', {'uname':uname,'id':uid,'imobjl':imobj,'slow':slow,},
                               context_instance=RequestContext(request))

def showimage(request,path):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    iml = schoolim.objects.filter(name=str(path))
    if len(iml)==1:
        im = schoolim.objects.get(name=str(path))
        if im.vistoall == False:
            if request.user.is_authenticated() and request.user.is_active:
                return render_to_response('stjoseph/showimage.html', {'uname':uname,'id':uid,'im':im,},
                               context_instance=RequestContext(request))
        else:
            return render_to_response('stjoseph/showimage.html', {'uname':uname,'id':uid,'im':im,},
                               context_instance=RequestContext(request))
    errormsg = "Either you don't have permission or the page does not exist!"
    return render_to_response('stjoseph/404.html', {'uname':uname,'id':uid,'errormsg':errormsg,},
                               context_instance=RequestContext(request))

def servethumb(request,path):
    iml = schoolim.objects.filter(name=str(path))
    if len(iml)==1:
        im = schoolim.objects.get(name=str(path))
        if im.vistoall == False:
            if request.user.is_authenticated() and request.user.is_active:
                return serve(request,path,settings.MEDIA_ROOT+'/thumb')
            else:
                raise Http404
        else:
            return serve(request,path,settings.MEDIA_ROOT+'/thumb')
    else:
        raise Http404    

def servephoto(request,path):
    iml = schoolim.objects.filter(name=str(path))
    if len(iml)==1:
        im = schoolim.objects.get(name=str(path))
        if im.vistoall == False:
            if request.user.is_authenticated() and request.user.is_active:
                return serve(request,path,settings.MEDIA_ROOT+'/snaps')
            else:
                raise Http404
        else:
            return serve(request,path,settings.MEDIA_ROOT+'/snaps')
    else:
        raise Http404 

def New_Capcha():
    cap_choice = ('+','-','*')
    cap_o = randint(0,2)
    cap_a = randint(5,9)
    cap_b = randint(0,4)
    cap_res = 0
    cap_msg = str(cap_a)+' '+str(cap_choice[cap_o])+' '+str(cap_b)+' = ?'
    if cap_o==0:
        cap_res = cap_a + cap_b
    elif cap_o==1:
        cap_res = cap_a - cap_b
    else:
        cap_res = cap_a * cap_b
    return (cap_msg,cap_res)

def changepass(request):
    uname = None
    uid = 0
    passup = False
    cpform = None
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
        if request.method == 'POST':
            cpform = CPForm(request.POST)
            if cpform.is_valid():
                if cpform.data['pas'] == cpform.data['cpas']:
                    cus = User.objects.get(username__exact=str(uid))
                    cus.set_password(str(cpform.data['pas']))
                    cus.save()
                    passup = True
                else:
                    cpform.errors['pas'] = "Passwords do not match"
                    cpform.errors['cpas'] = "Passwords do not match"
        else:
            cpform = CPForm()
    return render_to_response('stjoseph/changepass.html', {'uname':uname,'id':uid,'cpform':cpform,'passup':passup,'title':'Change Password',},
                               context_instance=RequestContext(request))

def SendResetMail(emailadd, uid, actnum):
    message = "Hello,\n\nYou can reset your password by clicking the link below:"
    message += "\n\nhttp://stjosephrbgj.org.in/newpass/"+str(uid)+'/'+str(actnum)+"/"
    message += "\n\nIf you have not requested for password reset, please ignore this mail."
    message += "\n\nThanks! :-)\n\n--\nWeb Admin\nSt. Joseph's Convent High School, Robertsganj"
    email = EmailMessage('Password Reset for St. Joseph', message, to=[emailadd])
    email.send()

def newpass(request,uid,actnum):
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/')
    rql = presrqst.objects.filter(pk=uid,actn=actnum)
    if len(rql)==1:
        passup = False
        cpform = None
        if request.method == 'POST':
            cpform = CPForm(request.POST)
            if cpform.is_valid():
                if cpform.data['pas'] == cpform.data['cpas']:
                    cus = User.objects.get(username__exact=str(uid))
                    cus.set_password(str(cpform.data['pas']))
                    cus.save()
                    passup = True
                    presrqst.objects.filter(pk=uid,actn=actnum).delete()
                else:
                    cpform.errors['pas'] = "Passwords do not match"
                    cpform.errors['cpas'] = "Passwords do not match"
        else:
            cpform = CPForm()
        return render_to_response('stjoseph/resetpass.html', {'uid':uid,'cpform':cpform,'passup':passup,'actnum':actnum,},
                           context_instance=RequestContext(request))
    else:
        oerror = 'Invalid or Used Link to reset the password!'
        return render_to_response('stjoseph/home.html', {'uname':None,'id':None, 'oerror':oerror},
                       context_instance=RequestContext(request))

def forgotpass(request):
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/')
    npsend = False
    capm = None
    if request.method == 'POST':
        fpform = FPForm(request.POST.copy())
        if fpform.is_valid():
            pass
        nerr=True
        cap_a = int(fpform.data['capq'][0])
        cap_b = int(fpform.data['capq'][4])
        if fpform.data['capq'][2]=='+':
            if str(cap_a+cap_b)!=str(fpform.data['cap']):
                fpform.errors['cap']='Captcha Error'
        elif fpform.data['capq'][2]=='-':
            if str(cap_a-cap_b)!=str(fpform.data['cap']):
                fpform.errors['cap']='Captcha Error'
        elif fpform.data['capq'][2]=='*':
            if str(cap_a*cap_b)!=str(fpform.data['cap']):
                fpform.errors['cap']='Captcha Error'
        for k in fpform.errors:
            if fpform.errors[k] != None:
                nerr = False
                break
        if nerr:
            rusl = sjcuser.objects.filter(email=fpform.data['email'].strip().lower(),act=True)
            if len(rusl)==1:
                cuid = rusl[0].id
                now = datetime.datetime.now()
                actnum = str(hashlib.sha224(now.strftime("%Y-%m-%d %H:%M")).hexdigest())
                rql = presrqst.objects.filter(pk=cuid)
                if len(rql)!=0:
                    rql.update(actn=actnum)
                else:
                    nrq = presrqst.objects.create(pk=cuid,actn=actnum)
                    nrq.save()
                SendResetMail(str(fpform.data['email']).strip().lower(), cuid, actnum)
                npsend = True
                return render_to_response('stjoseph/forgotpass.html', {'fpform':fpform,'npsend':npsend,},
                               context_instance=RequestContext(request))
            else:
                oerror = 'No Account with the given email address registered, or your account has not been activated!'
                return render_to_response('stjoseph/home.html', {'uname':None,'id':None, 'oerror':oerror},
                               context_instance=RequestContext(request))
        (capm,cap_res) = New_Capcha()
        fpform.data['capq'] = capm
        fpform.data['cap'] = None 
    else:
        (capm,cap_res) = New_Capcha()
        fpform = FPForm(initial={'capr':cap_res,'capq':capm})
    return render_to_response('stjoseph/forgotpass.html', {'fpform':fpform,'npsend':npsend,'capm':capm,},
                               context_instance=RequestContext(request))

def profile(request, uid):
    uname = None
    oerror = None
    cid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        cid = sus.id
        rusl = sjcuser.objects.filter(pk=uid,act=True)
        if len(rusl)==1:
            rus = sjcuser.objects.get(pk=uid)
            upro = False
            con = None
            if str(uid)==str(cid):
                upro = True
                con = rus.con
            clasc={"1":"LKG","2": "UKG","3": "I",
                     "4":"II","5": "III","6": "IV",
                     "7":"V","8": "VI","9": "VII",
                     "10":"VIII","11": "IX","12": "X",
                     }
            titc ={"1":"Alumni","2": "Student","3": "Staff","4": "Alumni & Staff"}
            propic = None
            if rus.lf:
                pattern = "((http://)|(https://))?(www\.)?facebook\.com/(profile\.php\?id=(?P<uid>[0-9]+)|(?P<un>[a-z0-9\.]+))"
                temp = re.match(pattern,rus.lf,flags=re.I)
                if temp:
                    if temp.group('uid'):
                        g_url = "https://graph.facebook.com/%s/picture?type=normal" % str(temp.group('uid'))
                    else:
                        g_url = "https://graph.facebook.com/%s/picture?type=normal" % str(temp.group('un'))
                    try:
                      propic = urllib2.urlopen(g_url).geturl()
                    except urllib2.HTTPError as e:
                      propic = None
            if rus.tit=="3":
                return render_to_response('stjoseph/profile.html', {'uname':uname,'name':rus.name,'email':rus.email,'propic':propic,
                        'tit':titc[rus.tit], 'yj':rus.yj,'subj':rus.subj, 'cw':rus.cw,'lf':rus.lf,'upro':upro,'con':con,'id':cid,},
                       context_instance=RequestContext(request))
            elif rus.tit=="4":
                return render_to_response('stjoseph/profile.html', {'uname':uname,'name':rus.name,'email':rus.email,'propic':propic,
                        'tit':titc[rus.tit],'cla':clasc[rus.cla],'yop':rus.yop,'yj':rus.yj,'subj':rus.subj, 'cw':rus.cw,'lf':rus.lf,'upro':upro,'con':con,'id':cid,},
                       context_instance=RequestContext(request))
            else:
                return render_to_response('stjoseph/profile.html', {'uname':uname,'name':rus.name,'email':rus.email,'propic':propic,
                        'tit':titc[rus.tit], 'cla':clasc[rus.cla],'yop':rus.yop, 'cw':rus.cw,'lf':rus.lf,'upro':upro,'con':con,'id':cid,},
                       context_instance=RequestContext(request))
        else:
            oerror = "User does not exist! O_o"    
    else:
        oerror = "You need to be logged in to view this page!"    
    return render_to_response('stjoseph/home.html', {'uname':uname,'id':cid, 'oerror':oerror},
                               context_instance=RequestContext(request))

def edit(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
        if request.method == 'POST':
            rform = RegisterForm(request.POST)
            if rform.is_valid():
                pass
            if rform.data['tit'] == "3":
                rform.errors['cla']=None
                rform.errors['yop']=None
            elif rform.data['tit'] == "4":
                pass
            else:
                rform.errors['yj']=None
                rform.errors['subj']=None
            rform.errors['name']=None
            rform.errors['email']=None
            rform.errors['pas']=None
            rform.errors['cpas']=None
            rform.errors['cap']=None
            rform.errors['capq']=None
            pattern = "http(s)?://(www\.)?facebook\.com/(profile\.php\?id=(?P<uid>[0-9]+)|(?P<un>[a-z0-9\.]+))"
            temp = re.match(pattern,rform.data['lf'],flags=re.I)
            if temp:
              pass
            else:
              rform.errors['lf'] = 'Error'
            nerr = True
            for k in rform.errors:
                if rform.errors[k] != None:
                    nerr = False
                    break
            if nerr:
                rus = sjcuser.objects.filter(pk=uid)
                rus.update(tit = rform.data['tit'])
                if rform.data['tit'] == "3":
                    rus.update(yj = rform.data['yj'])
                    rus.update(subj = rform.data['subj'])
                else:
                    rus.update(cla = rform.data['cla'])
                    rus.update(yop = rform.data['yop'])
                    if rform.data['tit'] == "4":
                        rus.update(yj = rform.data['yj'])
                        rus.update(subj = rform.data['subj'])
                rus.update(cw = rform.data['cw'])
                rus.update(lf = rform.data['lf'])
                rus.update(con = rform.data['con'])
                rdurl = '/profile/'+str(uid)+'/'
                return HttpResponseRedirect(rdurl)
            if rform.data['tit'] == "3":
                rform.fields['cla'].widget.attrs['disabled'] = 'true'
                rform.fields['yop'].widget.attrs['disabled'] = 'true'
            elif rform.data['tit'] == "4":
                pass
            else:
                rform.fields['yj'].widget.attrs['disabled'] = 'true'
                rform.fields['subj'].widget.attrs['disabled'] = 'true'
        else:
            if sus.tit == "3":
                rform = RegisterForm(initial={'tit': str(sus.tit),'yj':sus.yj,'subj':sus.subj,'cw':sus.cw,'lf':sus.lf,'con':sus.con,})
                rform.fields['cla'].widget.attrs['disabled'] = 'true'
                rform.fields['yop'].widget.attrs['disabled'] = 'true'
            elif sus.tit == "4":
                rform = RegisterForm(initial={'tit': str(sus.tit),'cla':sus.cla,'yop':sus.yop,'yj':sus.yj,'subj':sus.subj,'cw':sus.cw,'lf':sus.lf,'con':sus.con,})
                pass
            else:
                rform = RegisterForm(initial={'tit': str(sus.tit),'cla':sus.cla,'yop':sus.yop,'cw':sus.cw,'lf':sus.lf,'con':sus.con,})
                rform.fields['yj'].widget.attrs['disabled'] = 'true'
                rform.fields['subj'].widget.attrs['disabled'] = 'true'
        return render_to_response('stjoseph/edit.html', RequestContext(request, {
            'uname':uname,'id':uid,'form': rform,}))
    return render_to_response('stjoseph/edit.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def history(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    return render_to_response('stjoseph/history.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def song(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    return render_to_response('stjoseph/song.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def principal(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    return render_to_response('stjoseph/principal.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def information(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    return render_to_response('stjoseph/information.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def activities(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    return render_to_response('stjoseph/activities.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def infrastructure(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    return render_to_response('stjoseph/infrastructure.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def halloffame(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    return render_to_response('stjoseph/halloffame.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def alumni(request):
    uname = None
    uid = 0
    al_list = []
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
        al_list.extend(sjcuser.objects.filter(tit="1",act=True))
        al_list.extend(sjcuser.objects.filter(tit="4",act=True))
        clasc={"1":"LKG","2": "UKG","3": "I",
                     "4":"II","5": "III","6": "IV",
                     "7":"V","8": "VI","9": "VII",
                     "10":"VIII","11": "IX","12": "X",
                     }
        for ob in al_list:
            ob.cla = clasc[ob.cla]
        al_list = sorted(al_list, key=lambda sjcuser: sjcuser.name.lower())
    return render_to_response('stjoseph/alumni.html', {'uname':uname,'id':uid,'alumlist':al_list},
                               context_instance=RequestContext(request))
                               
def students(request):
    uname = None
    uid = 0
    st_list = []
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
        st_list.extend(sjcuser.objects.filter(tit="2",act=True))
        clasc={"1":"LKG","2": "UKG","3": "I",
                     "4":"II","5": "III","6": "IV",
                     "7":"V","8": "VI","9": "VII",
                     "10":"VIII","11": "IX","12": "X",
                     }
        for ob in st_list:
            ob.cla = clasc[ob.cla]
        st_list = sorted(st_list, key=lambda sjcuser: sjcuser.name.lower())
    return render_to_response('stjoseph/students.html', {'uname':uname,'id':uid,'stulist':st_list},
                               context_instance=RequestContext(request))

def staff(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    return render_to_response('stjoseph/staff.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def SendActMail(emailadd, actnum):
    message = "Hello,\n\nYour account has been created.\n\nActivate your account by clicking the link below:"
    message += "\n\nhttp://stjosephrbgj.org.in/activate/"+str(actnum)+"/"
    message += "\n\nThanks! :-)\n\n--\nWeb Admin\nSt. Joseph's Convent High School, Robertsganj"
    email = EmailMessage('Activation Mail for St. Joseph', message, to=[emailadd])
    email.send()

def MailWelcome(emailid):
    html_mes = 'Hello<br><br>We are pleased to have you registered on our website. <br><br>If you have not yet seen, the <i>website has its updated gallery</i> of school. You can also login and <i>find more people on the alumni, student and staff pages</i>.<br><br>This portal of ours will help us in:<br><ul><li>Maintaining a database of all related to school.</li><li>Conducting alumni meets in future.</li><li>Connect student, alumni and staff of school, so that they can ask/share information or anything.</li><li>Keep you informed of the latest happenings.<br></li></ul><b>What\'s Next?</b><br><br>There are few of things you could do:<br><ul><li><b>Keep Your profile updated</b>, with all the necessary information. You may not be able to update your email address or name from the website. At anytime you would like it to be updated, please mail the webadmin.<br>  </li><li><b>Mail us</b> anything you would like to put on website as blog or share with student, teachers or alumni of school. We will try to put it on our website, share in school, and on facebook.<br>  </li><li><b>Help us grow</b> by telling your friends to register on the website. This is required especially to make alumni meet possible.</li><li>We always welcome your <b>Suggestions/Comments</b> to improve.<br>  </li></ul>You can also communicate with the principal by mailing her at <a href="mailto:principal@stjosephrbgj.org.in" target="_blank">principal@stjosephrbgj.org.in</a><br><b><br>Information Regarding Profiles:<br></b><br>Few of the Alumni and Student are confused with the fields in the profile pages. We request you to please use the information below and update your profile:<br><ul><li><b>Title:</b> In this field, select student only if you are currently a student of St. Joseph\'s, else choose Alumni. While Staff choose Staff. For those who are both Staff and Alumni, please choose the corresponding option.</li><li><b>Class Last Attended:</b> This is required only for Students and Alumni. Students select the class you are presently in, while Alumni select the class you last attended in St. Joseph.</li><li><b>Year of Passing:</b> Students enter the year you would pass the class mentioned in Class Last Attended. Alumni choose the year you passed above class from SJC.</li><li><b>About me: </b>this can contain anything you would like to share with us, including your journey in the school, your current work information etc.</li><li><b>Link to Facebook:</b> This is a link to your fb profile. You can get the link to your profile by going to the profile page of your on fb and copying the url in url bar of browser. This will help your friends to find you easily.<br></li><li><b>Contact:</b> Your contact info. This won\'t be visible to anyone else on website. It would be used only in case its required.<br></li></ul>If you have filled the wrong information, you can update your profile by logging in to the website.<br><b><br></b>For any queries/help regarding website you can mail us at <a href="mailto:webadmin@stjosephrbgj.org.in" target="_blank">webadmin@stjosephrbgj.org.in</a><br><br>Thanks and Regards!<br><br>Web Admin<br>St. Joseph\'s Convent High School, Robertsganj<br><br><a href="http://stjosephrbgj.org.in/" target="_blank">http://stjosephrbgj.org.in/</a><br>'   
    email = EmailMessage('Welcome to St. Joseph\'s Convent High School, Robertsganj', html_mes, to=[emailid])
    email.content_subtype = "html"
    email.send()

def contact(request):
    uname = None
    uid = 0
    if request.user.is_authenticated() and request.user.is_active:
        sus = sjcuser.objects.get(email=request.user.email)
        uname = sus.name
        uid = sus.id
    return render_to_response('stjoseph/contact.html', {'uname':uname,'id':uid,},
                               context_instance=RequestContext(request))

def activate(request, actk):
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/')
    activated = False
    nsus = sjcuser.objects.filter(actn=str(actk),act=False)
    if len(nsus)!=0:
        sus = sjcuser.objects.get(actn=actk,act=False)
        nsus.update(act = True)
        user = User.objects.filter(email=sus.email)
        user.update(is_active = True)
        activated = True
        MailWelcome(sus.email)
        if sus.tit=="3" or sus.tit=="4":
            mes = "teacher registered with id = " + str(sus.id)
            email = EmailMessage('New Teacher Registered', mes, to=['webadmin@stjosephrbgj.org.in'])
            email.send()
    return render_to_response('stjoseph/home.html', {'activated':activated,},
                               context_instance=RequestContext(request))

def register(request):
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/')
    oerror = None
    cap_m = None
    if request.method == 'POST':
        rform = RegisterForm(request.POST.copy())
        if rform.is_valid():
            pass
        if rform.data['tit'] == "3":
            rform.fields['cla'].widget.attrs['disabled'] = 'true'
            rform.fields['yop'].widget.attrs['disabled'] = 'true'
            rform.errors['cla']=None
            rform.errors['yop']=None
        elif rform.data['tit'] == "4":
            pass
        else:
            rform.fields['yj'].widget.attrs['disabled'] = 'true'
            rform.fields['subj'].widget.attrs['disabled'] = 'true'
            rform.errors['yj']=None
            rform.errors['subj']=None
        nerr = True
        cap_a = int(rform.data['capq'][0])
        cap_b = int(rform.data['capq'][4])
        if rform.data['capq'][2]=='+':
            if str(cap_a+cap_b)!=str(rform.data['cap']):
                rform.errors['cap']='Captcha Error'
        elif rform.data['capq'][2]=='-':
            if str(cap_a-cap_b)!=str(rform.data['cap']):
                rform.errors['cap']='Captcha Error'
        elif rform.data['capq'][2]=='*':
            if str(cap_a*cap_b)!=str(rform.data['cap']):
                rform.errors['cap']='Captcha Error'
        for k in rform.errors:
            if rform.errors[k] != None:
                nerr = False
                break
        if rform.data['pas'] != rform.data['cpas']:
            rform.errors['pas'] = "Passwords do not match"
            rform.errors['cpas'] = "Passwords do not match"
            nerr = False
        temp = sjcuser.objects.filter(email=rform.data['email'].strip().lower())
        if len(temp) != 0:
            nerr = False
            oerror = "Email address entered is already registered! O_o"
            rform.errors['email'] = "invalid"
        pattern = "http(s)?://(www\.)?facebook\.com/(profile\.php\?id=(?P<uid>[0-9]+)|(?P<un>[a-z0-9\.]+))"
        tmp = re.match(pattern,rform.data['lf'],flags=re.I)
        if tmp:
          pass
        else:
          rform.errors['lf'] = 'Error'
          nerr = False
        if nerr:
            actk = hashlib.sha224(str(rform.data['email']).strip().lower()).hexdigest()
            if rform.data['tit'] == "3":
                nsus = sjcuser.objects.create(name=str(rform.data['name']).title(), email=str(rform.data['email']).strip().lower(), 
                    tit=rform.data['tit'], yj=rform.data['yj'], subj=rform.data['subj'], 
                    cw=rform.data['cw'], lf=rform.data['lf'], con=rform.data['con'], actn=str(actk))
            elif rform.data['tit'] == "4":
                nsus = sjcuser.objects.create(name=str(rform.data['name']).title(), email=str(rform.data['email']).strip().lower(), 
                    tit=rform.data['tit'], yj=rform.data['yj'], subj=rform.data['subj'], cla = rform.data['cla'], 
                    yop=rform.data['yop'], cw=rform.data['cw'], lf=rform.data['lf'], con=rform.data['con'], actn=str(actk))
            else:
                nsus = sjcuser.objects.create(name=str(rform.data['name']).title(), email=str(rform.data['email']).strip().lower(), 
                    tit=rform.data['tit'], cla = rform.data['cla'], yop=rform.data['yop'],
                    cw=rform.data['cw'], lf=rform.data['lf'], con=rform.data['con'], actn=str(actk))
            user = User.objects.create_user(str(nsus.id), str(rform.data['email']).strip().lower(), rform.data['pas'])
            user.is_staff = False
            user.is_active = False
            user.save()
            nsus.save()
            SendActMail(str(rform.data['email']).strip().lower(),actk)
            return render_to_response('stjoseph/register.html', RequestContext(request, {
                'registered': True,
            }))
        else:
            (capm,cap_res) = New_Capcha()
            rform.data['capq'] = capm
            rform.data['cap'] = None
    else:
        (capm,cap_res) = New_Capcha()
        rform = RegisterForm(initial={'capr':cap_res,'capq':capm})
        rform.fields['yj'].widget.attrs['disabled'] = 'true'
        rform.fields['subj'].widget.attrs['disabled'] = 'true'
    return render_to_response('stjoseph/register.html', RequestContext(request, {
        'form': rform, 'oerror': oerror,'capm':capm,
    }))

def loginu(request):
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/')
    oerror = None
    capm=None
    if request.method == 'POST':
        uname = None
        lform = LoginForm(request.POST.copy())
        nerr = True
        if lform.is_valid():
            pass
        cap_a = int(lform.data['capq'][0])
        cap_b = int(lform.data['capq'][4])
        if lform.data['capq'][2]=='+':
            if str(cap_a+cap_b)!=str(lform.data['cap']):
                lform.errors['cap']='Captcha Error'
        elif lform.data['capq'][2]=='-':
            if str(cap_a-cap_b)!=str(lform.data['cap']):
                lform.errors['cap']='Captcha Error'
        elif lform.data['capq'][2]=='*':
            if str(cap_a*cap_b)!=str(lform.data['cap']):
                lform.errors['cap']='Captcha Error'
        for k in lform.errors:
            if lform.errors[k] != None:
                nerr = False
                break
        if nerr:
            lsus = sjcuser.objects.filter(email=str(lform.data['email']).strip().lower())
            if len(lsus)==1:
                sus = sjcuser.objects.get(email=str(lform.data['email']).strip().lower())
                user = authenticate(username=str(sus.id), password=lform.data['pas'])
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        return HttpResponseRedirect('/')
                    else:
                        oerror = "Your account has not been activated! O_o"
                else:
                    oerror = "Invalid Login details! Are you registered yet? O_o"
            else:
                oerror = "Invalid Login details! Are you registered yet? O_o"
        (capm,cap_res) = New_Capcha()
        lform.data['capq'] = capm
        lform.data['cap'] = None
    else:
        (capm,cap_res) = New_Capcha()
        lform = LoginForm(initial={'capr':cap_res,'capq':capm})
    return render_to_response('stjoseph/login.html', {'oerror':oerror,'lform':lform,'capm':capm,},
       context_instance=RequestContext(request))

def logoutu(request):
    logout(request)
    return HttpResponseRedirect('/')
