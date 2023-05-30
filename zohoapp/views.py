from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.utils.text import capfirst
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import JsonResponse

def index(request):

    return render(request,'index.html')

def register(request):
   
    if request.method=='POST':

        first_name=capfirst(request.POST['fname'])
        last_name=capfirst(request.POST['lname'])
        username=request.POST['uname']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        email=request.POST['email1']
        phone = request.POST['phone']

      
        if password==cpassword:  #  password matching......
            if User.objects.filter(username=username).exists(): #check Username Already Exists..
                messages.info(request, 'This username already exists!!!!!!')
                return redirect('register')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                
                user.save()
                u = User.objects.get(id = user.id)

                company_details(contact_number = phone, user = u).save()
    
        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            print("Password is not Matching.. ") 
            return redirect('register')   
        return redirect('register')

    return render(request,'register.html')

def login(request):
        
    if request.method == 'POST':
        
        email_or_username = request.POST['emailorusername']
        password = request.POST['password']

        user = authenticate(request, username=email_or_username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('base')
        else:
            return redirect('/')

    return render(request, 'register.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='login')
def base(request):
   
    
    company = company_details.objects.get(user = request.user)
    context = {
                'company' : company
            }
    return render(request,'loginhome.html',context)

@login_required(login_url='login')
def view_profile(request):

    company = company_details.objects.get(user = request.user)
    context = {
                'company' : company
            }
    return render(request,'profile.html',context)

@login_required(login_url='login')
def edit_profile(request,pk):

    company = company_details.objects.get(id = pk)
    user1 = User.objects.get(id = company.user_id)

    if request.method == "POST":

        user1.first_name = capfirst(request.POST.get('f_name'))
        user1.last_name  = capfirst(request.POST.get('l_name'))
        user1.username = request.POST.get('uname')
        # pat.age = request.POST.get('age')
        # pat.address = capfirst(request.POST.get('address'))
        # pat.gender = request.POST.get('gender')
        # user1.email = request.POST.get('email')
        # pat.email = request.POST.get('email')
        # pat.contact_num = request.POST.get('cnum')
        # #fkey1= request.POST.get('doc')
        # #pat.doctor = doctor.objects.get(id = fkey1)
        # if len(request.FILES)!=0 :
        #     doc.profile_pic = request.FILES.get('file')


        company.save()
        user1.save()
        return redirect('view_profile')

    context = {
        'company' : company,
        'user1' : user1,
    }
    context = {
                'company' : company,
            }
    return render(request,'edit_profile.html',context)

@login_required(login_url='login')
def itemview(request):
    viewitem=AddItem.objects.all()
    return render(request,'item_view.html',{'view':viewitem})


@login_required(login_url='login')
def additem(request):
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    
    


  
    
        



    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'additem.html',{'unit':unit,'sale':sale,'purchase':purchase,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })

@login_required(login_url='login')
def add_account(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']
       
        acc=Purchase(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()                 
        return redirect("additem")
        
    return render(request,'additem.html')


@login_required(login_url='login')
def add(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            radio=request.POST.get('radio')
            if radio=='tax':
    
                
                inter=request.POST['inter']
                intra=request.POST['intra']
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                                )
                
            else:
                                                  
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate='none',intrastate='none'
                                )
                ad_item.save()
            ad_item.save()
           
            return redirect("itemview")
    return render(request,'additem.html')



@login_required(login_url='login')
def edititem(request,id):
    pedit=AddItem.objects.get(id=id)
    p=Purchase.objects.all()
    s=Sales.objects.all()
    u=Unit.objects.all()

    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))
    

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    return render(request,'edititem.html',{"account":account,"account_type":account_type,'e':pedit,'p':p,'s':s,'u':u,"accounts":accounts,"account_types":account_types})


@login_required(login_url='login')
def edit_db(request,id):
        if request.method=='POST':
            edit=AddItem.objects.get(id=id)
            edit.type=request.POST.get('type')
            edit.Name=request.POST['name']
            unit=request.POST['unit']
            edit.s_price=request.POST['sel_price']
            sel_acc=request.POST['sel_acc']
            edit.s_desc=request.POST['sel_desc']
            edit.p_price=request.POST['cost_price']
            cost_acc=request.POST['cost_acc']        
            edit.p_desc=request.POST['cost_desc']
            
            
            edit.unit=Unit.objects.get(id=unit)
            edit.sales=Sales.objects.get(id=sel_acc)
            edit.purchase=Purchase.objects.get(id=cost_acc)
            edit.save()
            return redirect('itemview')

        return render(request,'edititem.html')


@login_required(login_url='login')
def detail(request,id):
    user_id=request.user
    items=AddItem.objects.all()
    product=AddItem.objects.get(id=id)
    history=History.objects.filter(p_id=product.id)
    print(product.id)
    
    
    context={
       "allproduct":items,
       "product":product,
       "history":history,
      
    }
    
    return render(request,'demo.html',context)


@login_required(login_url='login')
def Action(request,id):
    user=request.user.id
    user=User.objects.get(id=user)
    viewitem=AddItem.objects.all()
    event=AddItem.objects.get(id=id)
    

    print(user)
    if request.method=='POST':
        action=request.POST['action']
        event.satus=action
        event.save()
        if action == 'active':
            History(user=user,message="Item marked as Active ",p=event).save()
        else:
            History(user=user,message="Item marked as inActive",p=event).save()
    return render(request,'item_view.html',{'view':viewitem})

@login_required(login_url='login')
def cleer(request,id):
    dl=AddItem.objects.get(id=id)
    dl.delete()
    return redirect('itemview')


@login_required(login_url='login')
def add_unit(request):
    if request.method=='POST':
        unit_name=request.POST['unit_name']
        Unit(unit=unit_name).save()
        return redirect('additem')
    return render(request,"additem.html")


@login_required(login_url='login')
def add_sales(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Sales(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect('additem')
    return render(request,'additem.html')


@login_required(login_url='login')
def vendor(request):
    return render(request,'create_vendor.html')



@login_required(login_url='login')
def add_vendor(request):
    if request.method=="POST":
        vendor_data=vendor_table()
        vendor_data.salutation=request.POST['salutation']
        vendor_data.first_name=request.POST['first_name']
        vendor_data.last_name=request.POST['last_name']
        vendor_data.company_name=request.POST['company_name']
        vendor_data.vendor_display_name=request.POST['v_display_name']
        vendor_data.vendor_email=request.POST['vendor_email']
        vendor_data.vendor_wphone=request.POST['w_phone']
        vendor_data.vendor_mphone=request.POST['m_phone']
        vendor_data.skype_number=request.POST['skype_number']
        vendor_data.designation=request.POST['designation']
        vendor_data.department=request.POST['department']
        vendor_data.website=request.POST['website']
        vendor_data.gst_treatment=request.POST['gst']

        x=request.POST['gst']
        if x=="Unregistered Business-not Registered under GST":
            vendor_data.pan_number=request.POST['pan_number']
            vendor_data.gst_number="null"
        else:
            vendor_data.gst_number=request.POST['gst_number']
            vendor_data.pan_number=request.POST['pan_number']

        vendor_data.source_supply=request.POST['source_supply']
        vendor_data.currency=request.POST['currency']
        vendor_data.opening_bal=request.POST['opening_bal']
        vendor_data.payment_terms=request.POST['payment_terms']

        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vendor_data.user=udata

        



        
        # vendor_data=vendor(user=udata,salutation=salutation,first_name=first_name,last_name=last_name,
        #     company_name=company_name,vendor_display_name=vendor_display_name,vendor_email=vendor_email,
        #     vendor_wphone=vendor_wphone,vendor_mphone=vendor_mphone,skype_number=skype_number,designation=designation,
        #     department=department,website=website,gst_treatment=gst_treatment,source_supply=source_supply,
        #     gst_number=gst_number,pan_number=pan_number,currency=currency,opening_bal=opening_bal,
        #     payment_terms=payment_terms)
        
        
        
        
        vendor_data.save()
        return redirect('base')
        

def sample(request):
    print("hello")
    return redirect('base')

def view_vendor_list(request):
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    data=vendor_table.objects.filter(user=udata)
    return render(request,'vendor_list.html',{'data':data})

def view_vendor_details(request,pk):
    user_id=request.user.id
    udata=User.objects.get(id=user_id)
    vdata1=vendor_table.objects.filter(user=udata)
    vdata2=vendor_table.objects.get(id=pk)
    mdata=mail_table.objects.filter(vendor=vdata2)
    ddata=doc_upload_table.objects.filter(user=udata,vendor=vdata2)

    return render(request,'vendor_details.html',{'vdata':vdata1,'vdata2':vdata2,'mdata':mdata,'ddata':ddata})

def add_comment(request,pk):
    if request.method=='POST':
        comment=request.POST['comment']
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vdata2=vendor_table.objects.get(id=pk)
        comments=comments_table(user=udata,vendor=vdata2,comment=comment)
        comments.save()
        return redirect("view_vendor_list")

def sendmail(request,pk):
    if request.method=='POST':
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vdata2=vendor_table.objects.get(id=pk)
        mail_from=settings.EMAIL_HOST_USER
        mail_to=request.POST['email']
        subject=request.POST['subject']
        content=request.POST['content']
        mail_data=mail_table(user=udata,vendor=vdata2,mail_from=mail_from,mail_to=mail_to,subject=subject,content=content)
        mail_data.save()

        subject = request.POST['subject']
        message = request.POST['content']
        recipient = request.POST['email']     #  recipient =request.POST["inputTagName"]
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

        return redirect("view_vendor_list")



def edit_vendor(request,pk):
    vdata=vendor_table.objects.get(id=pk)
    return render(request,'edit_vendor.html',{'vdata':vdata})

def edit_vendor_details(request,pk):
    if request.method=='POST':
        vdata=vendor_table.objects.get(id=pk)
        vdata.salutation=request.POST['salutation']
        vdata.first_name=request.POST['first_name']
        vdata.last_name=request.POST['last_name']
        vdata.company_name=request.POST['company_name']
        vdata.vendor_display_name=request.POST['v_display_name']
        vdata.vendor_email=request.POST['vendor_email']
        vdata.vendor_wphone=request.POST['w_phone']
        vdata.vendor_mphone=request.POST['m_phone']
        vdata.skype_number=request.POST['skype_number']
        vdata.designation=request.POST['designation']
        vdata.department=request.POST['department']
        vdata.website=request.POST['website']
        vdata.gst_treatment=request.POST['gst']
        if vdata.gst_treatment=="Unregistered Business-not Registered under GST":
            vdata.pan_number=request.POST['pan_number']
            vdata.gst_number="null"
        else:
            vdata.gst_number=request.POST['gst_number']
            vdata.pan_number=request.POST['pan_number']

        vdata.source_supply=request.POST['source_supply']
        vdata.currency=request.POST['currency']
        vdata.opening_bal=request.POST['opening_bal']
        vdata.payment_terms=request.POST['payment_terms']

        vdata.save()
        return redirect("view_vendor_list")

def upload_document(request,pk):
    if request.method=='POST':
        user_id=request.user.id
        udata=User.objects.get(id=user_id)
        vdata=vendor_table.objects.get(id=pk)
        title=request.POST['title']
        document=request.FILES.get('file')
        doc_data=doc_upload_table(user=udata,vendor=vdata,title=title,document=document)
        doc_data.save()
        return redirect("view_vendor_list")

def download_doc(request,pk):
    document=get_object_or_404(doc_upload_table,id=pk)
    response=HttpResponse(document.document,content_type='application/pdf')
    response['Content-Disposition']=f'attachment; filename="{document.document.name}"'
    return response

def cancel_vendor(request):
    return redirect("view_vendor_list")

def delete_vendor(request,pk):
    if comments_table.objects.filter(vendor=pk).exists():
        user2=comments_table.objects.filter(vendor=pk)
        user2.delete()
    if mail_table.objects.filter(vendor=pk).exists():
        user3=mail_table.objects.filter(vendor=pk)
        user3.delete()
    if doc_upload_table.objects.filter(vendor=pk).exists():
        user4=doc_upload_table.objects.filter(vendor=pk)
        user4.delete()
    user1=vendor_table.objects.get(id=pk)
    user1.delete()
    return redirect("view_vendor_list")
    
    

# view functions for retainer invoice

@login_required(login_url='login')
def add_customer(request):
    if request.method=='POST':
        customer_name=request.POST['name']
        address=request.POST['address']
        customer=customer(customer_name=customer_name,customer_address=address)
        customer.save()
        return redirect('add_invoice')
    return render(request,'add_customer.html')


@login_required(login_url='login')
def retainer_invoice(request):
    invoices=RetainerInvoice.objects.all()
    context={'invoices':invoices}
    return render(request,'retainer_invoice.html',context)



@login_required(login_url='login')
def add_invoice(request):
    customer=customer.objects.all()   
    context={'customer':customer,}    
    return render(request,'add_invoice.html',context)

@login_required(login_url='login')
def create_invoice_draft(request):
    
    if request.method=='POST':
        select=request.POST['select']
        customer_name=customer.objects.get(id=select)
        retainer_invoice_number=request.POST['retainer-invoice-number']
        references=request.POST['references']
        retainer_invoice_date=request.POST['invoicedate']
        total_amount=request.POST.get('total')
        customer_notes=request.POST['customer_notes']
        terms_and_conditions=request.POST['terms']
    
        retainer_invoice=RetainerInvoice(
            customer_name=customer_name,retainer_invoice_number=retainer_invoice_number,refrences=references,retainer_invoice_date=retainer_invoice_date,total_amount=total_amount,customer_notes=customer_notes,terms_and_conditions=terms_and_conditions)
    
        retainer_invoice.save()
        

        description = request.POST.getlist('description[]')
        amount =request.POST.getlist('amount[]')
        if len(description)==len(amount):
            mapped = zip(description,amount)
            mapped=list(mapped)
            for ele in mapped:
                created = Retaineritems.objects.get_or_create(description=ele[0],amount=ele[1], retainer=retainer_invoice)
        else:
            pass

        return redirect('retainer_invoice')

            
        

         
@login_required(login_url='login')
def create_invoice_send(request):
    if request.method=='POST':
        select=request.POST['select']
        customer_name=customer.objects.get(id=select)
        retainer_invoice_number=request.POST['retainer-invoice-number']
        references=request.POST['references']
        retainer_invoice_date=request.POST['invoicedate']
        total_amount=request.POST.get('total')
        customer_notes=request.POST['customer_notes']
        terms_and_conditions=request.POST['terms']
        retainer_invoice=RetainerInvoice(
        customer_name=customer_name,retainer_invoice_number=retainer_invoice_number,refrences=references,retainer_invoice_date=retainer_invoice_date,total_amount=total_amount,customer_notes=customer_notes,terms_and_conditions=terms_and_conditions,is_draft=False)
        retainer_invoice.save()

        description = request.POST.getlist('description[]')
        amount = request.POST.getlist('amount[]')
        if len(description)==len(amount):
            mapped = zip(description,amount)
            mapped=list(mapped)
            for ele in mapped:
                created = Retaineritems.objects.get_or_create(description=ele[0],amount=ele[1], retainer=retainer_invoice)
        else:
            pass
        return redirect('invoice_view',pk=retainer_invoice.id)



@login_required(login_url='login')
def invoice_view(request,pk):
    invoices=RetainerInvoice.objects.all()
    invoice=RetainerInvoice.objects.get(id=pk)
    item=Retaineritems.objects.filter(retainer=pk)

    context={'invoices':invoices,'invoice':invoice,'item':item}
    return render(request,'invoice_view.html',context)

@login_required(login_url='login')
def retainer_template(request,pk):
    invoice=RetainerInvoice.objects.get(id=pk)
    return render(request,'template.html',{'invoice':invoice})

@login_required(login_url='login')
def retainer_edit_page(request,pk):
    invoice=RetainerInvoice.objects.get(id=pk)
    customer=customer.objects.all()
    items=Retaineritems.objects.filter(retainer=pk)
    context={'invoice':invoice, 'customer':customer,'items':items}
    return render(request,'retainer_invoice_edit.html', context)


@login_required(login_url='login')
def retainer_update(request,pk):

    if request.method=='POST':
        retainer_invoice=RetainerInvoice.objects.get(id=pk)
        select=request.POST['select']
        retainer_invoice.customer_name=customer.objects.get(id=select)
        retainer_invoice.retainer_invoice_number=request.POST['retainer-invoice-number']
        retainer_invoice.refrences=request.POST['references']
        retainer_invoice.retainer_invoice_date=request.POST['invoicedate']
        retainer_invoice.total_amount=request.POST.get('total')
        retainer_invoice.customer_notes=request.POST['customer_notes']
        retainer_invoice.terms_and_conditions=request.POST['terms']
    
        retainer_invoice.save()
        
        descriptions=request.POST.getlist('description[]')
        amounts=request.POST.getlist('amount[]')
        # if len(descriptions)==len(amounts):
        #     mapped = zip(descriptions,amounts)
        #     mapped=list(mapped)
        #     for ele in mapped:
        #         created=Retaineritems.objects.filter(retainer=retainer_invoice).update(description=ele[0])
        # else:
        #     pass
        for i in range(len(descriptions)):
            description=descriptions[i]
            amount=amounts[i]
            obj,created=Retaineritems.objects.update_or_create(retainer=retainer_invoice,description=description,defaults={'amount':amount})
            obj.save()





        return redirect('retainer_invoice')

@login_required(login_url='login')
def mail_send(request,pk):

    if request.method=='POST':
        comments=request.POST.getlist('mailcomments')
        print(comments)
        files=request.FILES.getlist('files')
        email_to='alenantony32@gmail.com'
        subject='Retainer Invoice'
        message1=f'Please keep the attached\nretainer invoice for future use.\n\ncomments:\n'
        message2='' 

        for comment in comments:
            message2 += comment + '\n'

        messages=message1+message2    


        email=EmailMessage(
            subject=subject,
            body=messages,
            to=[email_to]
        )
        
        for file in files:
            email.attach(file.name, file.read(), file.content_type)

        email.send() 
        print('bottom') 
        retainer_invoice=RetainerInvoice.objects.get(id=pk)
        retainer_invoice.is_draft=False
        retainer_invoice.is_sent=True
        retainer_invoice.save()  
        return redirect('retainer_invoice')
    
    return redirect('retainer_invoice')

@login_required(login_url='login')
def retaineritem_delete(request,pk):
    print('delete')
    item = get_object_or_404(Retaineritems, id=pk)
    item.delete()
    print('deleted')
    return redirect('retainer_edit_page' ,pk=item.retainer.id)
    
@login_required(login_url='login')
def retainer_delete(request,pk):
    items=Retaineritems.objects.filter(retainer=pk)
    items.delete()
    retainer=RetainerInvoice.objects.get(id=pk)
    retainer.delete()
    return redirect('retainer_invoice')
        
            
#------------------------------------------

    
@login_required(login_url='login')
def view_sales_order(request):
    sales=SalesOrder.objects.all()
    return render(request,'view_sales_order.html',{"sale":sales})   

    
@login_required(login_url='login')
def create_sales_order(request):
    cust=customer.objects.all()
    pay=payment_terms.objects.all()
    itm=AddItem.objects.all()
    context={
        "c":cust,
        "pay":pay,
        "itm":itm,
    }
    return render(request,'create_sales_order.html',context)

    
@login_required(login_url='login')
def add_customer_for_sorder(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('myEmail')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

          
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("create_sales_order")

    
@login_required(login_url='login')        
def payment_term_for_sorder(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("create_sales_order")
        


@login_required(login_url='login')
def itemdata(request):
    cur_user = request.user.id
    user = User.objects.get(id=cur_user)
    company = company_details.objects.get(user = user)
    # print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
    
        
    item = AddItem.objects.get(Name=id)
    cus=customer.objects.get(customerName=cust)
    rate = item.s_price
    place=company.state
    gst = item.intrastate
    igst = item.interstate
    desc=item.s_desc
    print(place)
    mail=cus.customerEmail
    
    place_of_supply = customer.objects.get(customerName=cust).placeofsupply
    print(place_of_supply)
    return JsonResponse({"status":" not",'mail':mail,'desc':desc,'place':place,'rate':rate,'pos':place_of_supply,'gst':gst,'igst':igst})
    return redirect('/')
            



    
@login_required(login_url='login')
def add_sales_order(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            c=request.POST['cx_name']
            cus=customer.objects.get(customerName=c)   
            custo=cus.id
            sales_no=request.POST['sale_no']
            terms=request.POST['term']
            term=payment_terms.objects.get(id=terms)
            reference=request.POST['ord_no']
            sa_date=request.POST['sa_date']
            sh_date=request.POST['sh_date']
            d_method=request.POST['d_meth']
            s_pers=request.POST['s_pers']
        
            
            cxnote=request.POST['customer_note']
            subtotal=request.POST['subtotal']
            igst=request.POST['igst']
            cgst=request.POST['cgst']
            sgst=request.POST['sgst']
            totaltax=request.POST['totaltax']
            t_total=request.POST['t_total']
            if request.FILES.get('file') is not None:
                file=request.FILES['file']
            else:
                file="/static/images/alt.jpg"
            tc=request.POST['ter_cond']

            status=request.POST['sd']
            if status=='draft':
                print(status)   
            else:
                print(status)  
        
            product=request.POST.getlist('item[]')
            hsn=request.POST.getlist('hsn[]')
            quantity=request.POST.getlist('quantity[]')
            rate=request.POST.getlist('rate[]')
            desc=request.POST.getlist('desc[]')
            tax=request.POST.getlist('tax[]')
            total=request.POST.getlist('amount[]')
            term=payment_terms.objects.get(id=term.id)

            sales=SalesOrder(customer_id=custo,sales_no=sales_no,terms=term,reference=reference, sales_date=sa_date,ship_date=sh_date,
                        cxnote=cxnote,subtotal=subtotal,igst=igst,cgst=cgst,sgst=sgst,t_tax=totaltax,
                        grandtotal=t_total,status=status,terms_condition=tc,file=file,d_method=d_method,s_person=s_pers)
            sales.save()
            sale_id=SalesOrder.objects.get(id=sales.id)
            if len(product)==len(quantity)==len(tax)==len(total)==len(rate):

                mapped = zip(product,quantity,tax,total,rate)
                mapped = list(mapped)
                for element in mapped:
                    created =sales_item.objects.get_or_create(sale=sale_id,product=element[0],
                                        quantity=element[1],tax=element[2],total=element[3],rate=element[4])
                

                    
               
   
    return render(request,'create_sales_order.html')            
    
@login_required(login_url='login')
def sales_order_det(request,id):
    sales=SalesOrder.objects.get(id=id)
    saleitem=sales_item.objects.filter(sale_id=id)
    sale_order=SalesOrder.objects.all()
    company=company_details.objects.get(user_id=request.user.id)
    
    
    context={
        'sale':sales,
        'saleitem':saleitem,
        'sale_order':sale_order,
        'comp':company,
        
        
                    }
    return render(request,'sales_order_det.html',context)

    
@login_required(login_url='login')
def delet_sales(request,id):
    d=SalesOrder.objects.get(id=id)
    d.delete()
    return redirect('view_sales_order')
    
    
@login_required(login_url='login')
def edit_sales_order(request,id):
    c = customer.objects.all()
    itm = AddItem.objects.all()
    salesitem = sales_item.objects.filter(sale_id=id)
    sales = SalesOrder.objects.get(id=id)
    pay=payment_terms.objects.all()


    if request.method == 'POST':
        u=request.user.id
        c=request.POST['cx_name']
        
        cust=customer.objects.get(customerName=c) 
        sales.customer=cust
        term=request.POST['term']
        
        
        sales.terms = payment_terms.objects.get(id=term)
        sales.sales_date = request.POST['sa_date']
        sales.shipdate=request.POST['sh_date']
        sales.cxnote = request.POST['customer_note']
        sales.igst = request.POST['igst']
        sales.cgst = request.POST['cgst']
        sales.sgst = request.POST['sgst']
        sales.t_tax = request.POST['totaltax']
        sales.grandtotal = request.POST['t_total']

        if request.FILES.get('file') is not None:
            sales.file = request.FILES['file']
        else:
            sales.file = "/static/images/alt.jpg"

            sales.terms_condition = request.POST.get('ter_cond')
        
        status=request.POST['sd']
        if status=='draft':
            sales.status=status      
        else:
            sales.status=status   
         
        sales.save()
        
        product=request.POST.getlist('item[]')
        quantity=request.POST.getlist('quantity[]')
        rate=request.POST.getlist('rate[]')
        tax=request.POST.getlist('tax[]')
        total=request.POST.getlist('amount[]')
        obj_dele=sales_item.objects.filter(sale_id=sales.id)
        obj_dele.delete()
       
        if len(product)==len(quantity)==len(tax)==len(total)==len(rate):

            mapped = zip(product,quantity,tax,total,rate)
            mapped = list(mapped)
            for element in mapped:
                created = sales_item.objects.get_or_create(sale=sales,product=element[0],
                                    quantity=element[1],tax=element[2],total=element[3],rate=element[4])
                
            return redirect('sales_order_det',id)
    context={
        "c":c,
        "itm":itm,
        "saleitm":salesitem,
        "sale":sales,
        "pay":pay

    }
    return render(request,'edit_sale_page.html',context)
