from django.shortcuts import render, redirect, get_object_or_404
from .models import PvzLocation, Order, OrderItem, Delivery, PurchasedItem, ReturnedItem
from django.core.paginator import Paginator
from datetime import datetime
from openpyxl import Workbook
from django.http import HttpResponse
from .forms import PvzLocationForm, UserRegisterForm
import csv

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'main/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def index(request):
    pvz_list = PvzLocation.objects.all()
    return render(request, 'main/index.html', {'pvz_list': pvz_list})

def about(request, pvz_id):
    pvz = get_object_or_404(PvzLocation, id=pvz_id)
    orders = pvz.orders.filter(is_processed=False)

    order_number = request.GET.get("order_number")
    creation_date = request.GET.get("creation_date")
    total_cost = request.GET.get("total_cost")

    if order_number:
        orders = orders.filter(order_number__icontains=order_number)
    if creation_date:
        orders = orders.filter(creation_date=creation_date)
    if total_cost:
        orders = orders.filter(total_cost__gte=total_cost)

    for order in orders:
        order.total_weight = sum(item.item_weight for item in order.items.all())
        order.total_cost = sum(item.item_cost for item in order.items.all())
        order.save()

    return render(request, "main/about.html", {"pvz": pvz, "orders": orders})


def tracking(request):
    deliveries = Delivery.objects.all()
    return render(request, 'main/tracking.html', {'deliveries': deliveries})

def receipts(request):
    pvz_locations = PvzLocation.objects.all()
    return render(request, 'main/receipts.html', {'pvz_locations': pvz_locations})

def add_receipt(request):
    if request.method == 'POST':
        pvz_id = request.POST['pvz']
        pvz = get_object_or_404(PvzLocation, id=pvz_id)

        # Создание заказа
        order = Order.objects.create(
            pvz=pvz,
            order_number=request.POST['order_number'],
            sender_name=request.POST['sender_name'],
            sender_contact=request.POST['sender_contact'],
            creation_date=request.POST['creation_date']
        )

        # Создание товаров
        items = []
        item_count = 0
        while True:
            # Проверяем, есть ли данные для очередного товара
            item_name = request.POST.get(f'items[{item_count}][name]')
            item_weight = request.POST.get(f'items[{item_count}][weight]')
            item_cost = request.POST.get(f'items[{item_count}][cost]')
            if not item_name or not item_weight or not item_cost:
                break

            # Создаём объект товара
            items.append(OrderItem(
                order=order,
                item_name=item_name,
                item_weight=item_weight,
                item_cost=item_cost
            ))
            item_count += 1

        # Сохраняем все товары разом
        OrderItem.objects.bulk_create(items)

        # Перенаправляем на список заказов
        return redirect('order_list')

    # Выводим форму для добавления
    pvz_list = PvzLocation.objects.all()
    return render(request, 'main/receipts.html', {'pvz_list': pvz_list})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'main/orders.html', {'orders': orders})

def success_page(request):
    return render(request, 'main/success.html', {})


def check_order(request, order_id):
    # Получение заказа по ID
    order = get_object_or_404(Order, id=order_id)

    # Обработка отправки формы
    if request.method == 'POST':
        payment_status = request.POST.get('payment_status')
        recipient_name = request.POST.get('recipient_name')
        recipient_contact = request.POST.get('recipient_contact')
        acceptance_date = request.POST.get('acceptance_date')

        # Проверка, существует ли уже запись в Delivery
        delivery, created = Delivery.objects.get_or_create(
            order=order,
            defaults={
                'payment_status': payment_status,
                'recipient_name': recipient_name,
                'recipient_contact': recipient_contact,
                'acceptance_date': acceptance_date,
            }
        )

        if not created:
            # Обновление существующей записи
            delivery.payment_status = payment_status
            delivery.recipient_name = recipient_name
            delivery.recipient_contact = recipient_contact
            delivery.acceptance_date = acceptance_date
            delivery.save()

        # Помечаем заказ как обработанный
        order.is_processed = True
        order.save()

        return redirect('success_page')

    order_items = order.items.all()

    # Реализация пагинации
    paginator = Paginator(order_items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/check_order.html', {
        'order': order,
        'page_obj': page_obj
    })


def issued_orders(request):
    deliveries = Delivery.objects.filter(issued=True)

    return render(request, 'main/issued_orders.html', {'deliveries': deliveries})

def issue_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()

    if request.method == "POST":
        # Получаем список ID выбранных товаров
        issued_item_ids = request.POST.getlist('issued_items')

        # Разделяем товары на выданные и возвращённые
        issued_items = items.filter(id__in=issued_item_ids)
        returned_items = items.exclude(id__in=issued_item_ids)

        # Сохраняем выданные товары в таблицу "Купленные товары"
        for item in issued_items:
            PurchasedItem.objects.create(
                order=order,
                item_name=item.item_name,
                item_weight=item.item_weight,
                item_cost=item.item_cost
            )

        # Сохраняем оставшиеся товары в таблицу "Возвращённые товары"
        for item in returned_items:
            ReturnedItem.objects.create(
                order=order,
                item_name=item.item_name,
                item_weight=item.item_weight,
                item_cost=item.item_cost
            )

        # Помечаем заказ как выданный
        delivery = order.delivery
        delivery.issued = True
        delivery.save()

        return redirect('tracking')  

    return render(request, 'main/issue_order.html', {'order': order, 'items': items})

def success_page(request):
    return render(request, 'main/success.html', {})

def purchased_items(request):
    purchased_items = PurchasedItem.objects.all()

    return render(request, 'main/purchased_items.html', {'purchased_items': purchased_items})

def returned_items(request):
    returned_items = ReturnedItem.objects.all()

    return render(request, 'main/returned_items.html', {'returned_items': returned_items})

def export_import(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    action = request.GET.get('action')

    # Проверяем корректность ввода дат
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("Неверный формат даты. Используйте ГГГГ-ММ-ДД.")

    # Фильтруем заказы по диапазону дат
    orders = Order.objects.filter(creation_date__range=(start_date, end_date))

    # Если выбран Excel
    if action == "excel":
        from openpyxl import Workbook

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Заказы"

        # Заголовок таблицы
        headers = ["Номер заказа", "ПВЗ", "Имя отправителя", "Контакт", "Дата создания", "Общий вес", "Общая стоимость"]
        sheet.append(headers)

        for order in orders:
            sheet.append([
                order.order_number,
                order.pvz.name if order.pvz else "—",
                order.sender_name,
                order.sender_contact,
                order.creation_date,
                order.total_weight,
                order.total_cost,
            ])

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f"attachment; filename=Orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        workbook.save(response)
        return response

    if action == "csv":
        orders = Order.objects.filter(creation_date__range=(start_date, end_date))
        response = HttpResponse(content_type='text/csv')
        
        # Указываем правильную кодировку для Excel и других программ
        response['Content-Disposition'] = f'attachment; filename=Orders_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

        # Устанавливаем кодировку UTF-8 с BOM для Excel
        response.charset = 'utf-8-sig'

        writer = csv.writer(response)
        headers = ["Номер заказа", "ПВЗ", "Имя отправителя", "Контакт", "Дата создания", "Общий вес", "Общая стоимость"]
        writer.writerow(headers)

        # Заполнение данных
        for order in orders:
            writer.writerow([
                order.order_number,
                order.pvz.name if order.pvz else "—",
                order.sender_name,
                order.sender_contact,
                order.creation_date,
                order.total_weight,
                order.total_cost,
            ])
        return response

    return HttpResponse("Некорректное действие.")

def export_orders(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Фильтрация данных на основе дат
    deliveries = Delivery.objects.all()
    if start_date:
        deliveries = deliveries.filter(acceptance_date__gte=start_date)
    if end_date:
        deliveries = deliveries.filter(acceptance_date__lte=end_date)

    # Создание Excel-файла
    wb = Workbook()
    ws = wb.active
    ws.title = "Выданные заказы"

    headers = ["Номер заказа", "Статус оплаты", "Получатель", "Контакт", "Дата приёма заказа", "Статус"]
    ws.append(headers)

    # Добавление данных
    for delivery in deliveries:
        status = "Выдан" if delivery.issued else "Ожидает выдачи"
        ws.append([
            delivery.order.order_number,
            delivery.payment_status,
            delivery.recipient_name,
            delivery.recipient_contact,
            delivery.acceptance_date.strftime('%Y-%m-%d'),
            status
        ])

    # Настройка ответа с Excel-файлом
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Orders_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

    wb.save(response)
    return response

def add_pvz(request):
    if request.method == "POST":
        form = PvzLocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PvzLocationForm()

    return render(request, 'main/add_pvz.html', {'form': form})

def pvz_list(request):
    pvz_list = PvzLocation.objects.all()
    return render(request, 'main/pvz_list.html', {'pvz_list': pvz_list})