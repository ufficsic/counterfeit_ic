from counterfeit_ic import app, db, pimage, pspec, archives
from flask import render_template, redirect, session, request, url_for, flash, abort
from openpyxl import load_workbook
from user.models import User
from inventory.models import Manufacturer, Product, DefectType, Chip, Sample, Defect
from inventory.forms import CreateComponentsForm, AddComponentsForm
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from user.decorators import contributor_required, approval_required

import pyexcel as excel
import zipfile
import os
import shutil
import glob
import datetime
import pathlib
import logging


@app.route('/create/manufacturer', methods=('GET', 'POST'))
@contributor_required
def create_manufacturer():
    return render_template('inventory/create_manufacturer.html')


@app.route('/create/components', methods=('GET', 'POST'))
@contributor_required
def create_components():
    form = CreateComponentsForm()
    if form.validate_on_submit() and ('pspec', 'pimage', 'archive' in request.files):
        manufacturer = process_manufacturer(form)
        product = process_product(form, request, manufacturer)
        chip = get_or_create_model(Chip, user=session.get(
            'id'), manufacturer=manufacturer.id, product=product.id)
        sample = create_sample(chip)
        print('----------------------------------------------------------')
        print(manufacturer)
        print(product)
        print(chip)
        print(sample)
        print('----------------------------------------------------------')
        processed_count, error_count = process_archive(
            request, manufacturer, product, chip, sample)
        if error_count > 0:
            error = '{} files successfully added. {} files ignored.'.format(
                processed_count, error_count)
            flash(error, 'error')
        else:
            success = '{} files successfully added.'.format(processed_count)
            flash(success, 'success')
    return render_template('inventory/create_components.html', form=form)


def process_manufacturer(form):
    return get_or_create_model(
        Manufacturer,
        name=form.manufacturer.data
    )


def process_product(form, request, manufacturer):
    pspec_file = request.files.getlist('pspec')[0]
    pimage_file = request.files.getlist('pimage')[0]
    logging.info(pspec_file)
    logging.info(pimage_file)
    pspec_path = pspec.save(pspec_file)
    logging.info(pspec_path)
    pimage_path = pimage.save(pimage_file)
    logging.info(pimage_path)
    product = Product(
        name=form.product.data,
        manufacturer_id=manufacturer.id,
        spec_file_name=pspec_path,
        spec_image_name=pimage_path,
    )
    db.session.add(product)
    db.session.flush()
    return product


def create_sample(chip):
    sample = Sample(chip_id=chip.id)
    db.session.add(sample)
    return sample


def get_or_create_model(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.flush()
    return instance


@app.route('/create/add_files', methods=('GET', 'POST'))
@contributor_required
def add_files():
    form = CreateComponentsForm()
    if form.validate_on_submit():  # and 'photo' in request.files:
        if('photo', 'pdf' in request.files):
            pname = request.files.getlist('photo')[0]
            pname = pimage.save(pname)
            dname = request.files.getlist('pdf')[0]
            dname = pspec.save(dname)
            pass
    else:
        flash('Files could not be added!', 'error')
    return render_template('inventory/create_product.html', form=form)


def process_archive(request, manufacturer, product, chip, sample):
    temp = app.config['TEMP']
    image_folder = app.config['IMAGE_FOLDER']
    defect_image_folder = app.config['DEFECT_IMAGE_FOLDER']
    destination = datetime.datetime.now().strftime('%Y%m%d')
    row_start = app.config['ROW_START']
    path = os.path.join(app.config['APP_ROOT'], 'static')
    delim = '_'
    archive = request.files.getlist('archive')[0]

    old_working_directory = os.getcwd()
    os.chdir(path)

    if (os.path.isdir(temp)):
        shutil.rmtree(temp)

    index = None
    zfile = zipfile.ZipFile(archive, "r")
    zfile.extractall(os.path.join(temp))
    if (not os.path.isdir(os.path.join(image_folder, defect_image_folder, destination))):
        index = 0
        pathlib.Path(
            os.path.join(image_folder, defect_image_folder, destination)
        ).mkdir(parents=True, exist_ok=True)
    else:
        index = len(os.listdir(os.path.join(
            image_folder, defect_image_folder, destination)))

    xfiles = glob.glob(os.path.join(temp, '*.xlsx'))
    xfile = xfiles[0] if (xfiles) else None
    wb = load_workbook(filename=xfile)
    ws = wb.get_sheet_by_name(wb.sheetnames[0])

    error_count = 0
    processed_count = 0
    for row in range(row_start, ws.max_row+1):
        try:
            sample_id = ws.cell(row=row, column=1).value
            defect = ws.cell(row=row, column=2).value
            image = ws.cell(row=row, column=3).value
            defect_name = defect.split('|', 2)[0].strip()
            primary_type = defect.split('|', 2)[1].strip()
            secondary_type = defect.split('|', 2)[2].strip()
            image_path = os.path.join(temp, image).replace("\\", "/")
            img_ext = os.path.splitext(image_path)[1].lower()

            print('---------------image_path---------------')
            print(image_path)
            print('-------------------------------------------------')
            # print(image_path)
            if (not os.path.isfile(image_path)):
                logging.info("Image path doesn't exist: " + image_path)
                continue

            manufacturer_name = manufacturer.name if (
                len(manufacturer.name) <= 10) else manufacturer.name[0:10]
            product_name = product.name if (
                len(product.name) <= 10) else product.name[0:10]
            secure_image = secure_filename(
                manufacturer_name + delim + product_name + delim +
                defect_name.lower() + delim + str(index) + img_ext
            )
            dest = os.path.join(
                destination,
                secure_image
            ).replace("\\", "/")

            os.rename(image_path, os.path.join(
                image_folder, defect_image_folder, dest))
            index += 1
            defect_type = get_or_create_model(
                DefectType,
                name=defect_name,
                primary_type=primary_type,
                secondary_type=secondary_type
            )
            defect = Defect(
                chip_id=chip.id,
                sample_id=sample.id,
                defect_type_id=defect_type.id,
                defect_image_name=dest
            )
            db.session.add(defect)
            processed_count += 1
        except Exception as exception:
            logging.error(exception)
            error_count += 1
    if (processed_count > 0):
        db.session.commit()
    os.chdir(old_working_directory)
    return (processed_count, error_count)


@app.route('/add/components', methods=('GET', 'POST'))
@contributor_required
def add_components():
    error = None
    notification = None
    form = AddComponentsForm()
    manufacturers = Manufacturer.query.all()
    if (form.validate_on_submit() and ('archive' in request.files)):
        manufacturer_id = int(request.form.get('manufacturer'))
        product_id = int(request.form.get('product'))
        if (manufacturer_id == -1 or product_id == -1):
            error = 'Manufacturer or Product not selected'
            flash(error, 'error')
        else:
            manufacturer = Manufacturer.query.filter_by(
                id=manufacturer_id
            ).first()
            product = Product.query.filter_by(
                id=product_id
            ).first()
            chip = get_or_create_model(
                Chip, user=session.get('id'),
                manufacturer=manufacturer.id, product=product.id
            )
            sample = create_sample(chip)
            processed_count, error_count = process_archive(
                request, manufacturer, product, chip, sample)
            if error_count > 0:
                error = '{} files successfully added. {} files ignored.'.format(
                    processed_count, error_count)
                flash(error, 'error')
            else:
                success = '{} files successfully added.'.format(
                    processed_count)
                flash(success, 'success')
    return render_template(
        'inventory/add_components.html',
        manufacturers=manufacturers,
        form=form,
    )
    # form = CreateComponentsForm()
    # error = None
    # print(app.config['TEMP'])
    # if form.validate_on_submit() and ('pspec', 'pimage', 'archive' in request.files):
    #     print(list(request.files.to_dict().keys()))
    #     manufacturer = process_manufacturer(form)
    #     product = process_product(form, request, manufacturer)
    #     defect = process_archive(request, manufacturer, product)
    #     db.session.flush()
    #     if defect.id:
    #         db.session.commit()
    #     else:
    #         db.session.rollback()
    #         error = 'Error Uploading the file.'
    # return render_template('inventory/create_components.html', error=error, form=form)

    # row_start = 68
    # form = CreateComponentsForm()
    # error = None
    # print(dir(fe))
    # path = os.path.join(os.sep, app.config['APP_ROOT'], url_for('static', filename='tmp/'))

    # for i in os.listdir(os.path.join(path, 'tmp')):
    #     print(i)
    # os.chdir(owd)

    # print(os.getcwd())

    # file_rename = os.path.join(path, 'tmp','credila.png')

    # path =

    # img_folder = datetime.datetime.now().strftime('%Y%m%d')

    # temp = 'tmp'
    # image_main = 'images'
    # defect_image_folder = 'defect_images'
    # destination = datetime.datetime.now().strftime('%Y%m%d')
    # destination = '20171230'
    # row_start = 68
    # manufacturer = 'hello'
    # product = 'world'
    # delim = '_'
    # path = os.path.join(app.config['APP_ROOT'], 'static')

    # owd = os.getcwd()
    # os.chdir(path)

    # if (os.path.isdir('tmp')):
    #     shutil.rmtree('tmp')
    # index = (0 if (not os.path.isdir(os.path.join(image_main, defect_image_folder, destination)))
    #          else len(os.listdir(os.path.join(image_main, defect_image_folder, destination))))
    # print(index)

    # xfiles = glob.glob(os.path.join(temp, '*.xlsx'))
    # xfile = xfiles[0] if (xfiles) else None
    # print('---------------', xfile)
    # wb = load_workbook(filename=xfile)
    # ws = wb.get_sheet_by_name(wb.sheetnames[0])

    # for row in range(row_start, ws.max_row + 1):
    #     sample_id = ws.cell(row=row, column=1).value
    #     defect = ws.cell(row=row, column=2).value
    #     image = ws.cell(row=row, column=3).value
    #     defect_name = defect.split('|')[0].strip().lower()
    #     image_path = os.path.join(path, image)
    #     img_ext = os.path.splitext(image_path)[1].lower()
    #     print('defect : ', defect.split('|')[0].strip())

    #     manufacturer = 'hello' if (
    #         len(manufacturer) <= 10) else manufacturer[0:10]
    #     product = 'world' if (len(product) <= 10) else product[0:10]
    #     src = os.path.join(temp, image)
    #     dest = os.path.join(
    #         image_main,
    #         defect_image_folder,
    #         destination,
    #         (manufacturer + delim + product + delim +
    #          defect_name + delim + str(index) + img_ext)
    #     )
    #     index += 1

    #     print(src, dest)

    #     os.rename(src, dest)

    # image_defect = UploadSet(os.path.join(img_folder), IMAGES)
    # configure_uploads(app, (image_defect,))
    # print(image_defect)
    # name = image_defect.save(FileStorage(open(file_rename, 'rb')))
    # print(name)

    # dirList = os.walk(path)
    # for (dirpath, dirnames, filenames) in dirList:
    #     # print(dirpath)
    #     # print(dirnames, filenames)
    #     name = filenames[0]
    #     dirname = os.path.dirname(name)
    #     print(dirname)
    #     # if not os.path.exists(dirname):
    #     #     os.makedirs(dirname)
    #     # with open(name, 'rb') as f:
    #     #     print(f)

    # for file in files:
    #     wb = load_workbook(filename = file)
    #     ws = wb.get_sheet_by_name(wb.sheetnames[0])
    #     print(ws.max_row)
    #     for row in range(row_start, ws.max_row+1):
    #         sample_id = ws.cell(row=row,column=1).value
    #         defect = ws.cell(row=row,column=2).value
    #         image = ws.cell(row=row,column=3).value
    #         image_path = os.path.join(path, image)
    #         img_ext = os.path.splitext(image_path)[1]
    #         print('---------------')
    #         file_rename = os.path.join(path, 'Credila' + img_ext.lower())
    #         os.rename(image_path, file_rename)
    #         print(os.path.basename(path))
    #         print(os.path.dirname(path))
    #         print(os.path.relpath(path))

    # dirname = os.path.dirname(file_rename)
    # if not os.path.exists(dirname):
    #     os.makedirs(dirname)
    # with open(file_rename, 'rb') as f:
    #     print(FileStorage(f))
    #     name = photos.save(FileStorage(open(file_rename, 'rb')))
    #     print(name)

    # pic = ws.cell(row=68, column=3).hyperlink
    # print('is path : ', os.path.islink(pic.target))
    # print(url_for(pic.target))
    # name = photos.save(pic)
    # print(name)

    # sheet = excel.get_sheet(filename = file)
    # print( sheet.column['sample_id'])

    # for row in sheet.rows:
    #     for cell in row:
    #         print(cell.value)

    # path = os.path.join(app.config['APP_ROOT'], 'static', 'tmp')
    # print('path is : ', path)
    # if form.validate_on_submit(): # and 'photo' in request.files:
    #     if('archive' in request.files):
    #         name = request.files.getlist('archive')[0]
    #         print(name)
    #         zfile = zipfile.ZipFile(name, "r")
    #         path = os.path.join(app.config['APP_ROOT'], 'static', 'tmp')
    #         print('path is : ', path)
    #         zfile.extractall(path)
    #         # sample_form = [f for f in os.listdir(path) if f.endswith('.xlsx')][0]
    #         files = glob.glob(os.path.join(path, '*.xlsx'))[0]
    #         for file in files:
    #             print('---------------',file)
    #             wb = load_workbook(filename = file)
    #             sheet = wb.get_sheet_by_name(wb.sheetnames[0])
    #             print(sheet)

    # for name in zfile.namelist():
    #     if (name.endswith('xlsx')):
    #         # print('path is :', path)
    #         sampleForm = zfile.open(name, 'r')
    #         print(sampleForm.readlines())
    # print(er.get_array(zname))
    # with open(name) as f:
    #     content = f.readlines()
    #     print('-----------------')
    #     print(content)
    # return render_template('inventory/sample.html', archives=archives, error=error, form=form)
