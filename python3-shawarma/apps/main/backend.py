import pandas as pd
from shaw_queue.models import Menu, MenuCategory, MacroProduct, SizeOption, ContentOption, MacroProductContent, ProductVariant, ProductOption


def excel_to_base(excel):
    workbook = pd.read_excel(excel, sheet_name=0)
    workbook.head()

    for i in range(1, workbook.shape[0]):
        print(workbook.iloc[i, 0])
        #   menu
        menu_obj = Menu.objects.filter(pk=int(workbook.iloc[i, 1])).last()
        if not menu_obj:
            menu_obj = Menu.objects.create(id=int(workbook.iloc[i, 1]),
                                           title=workbook.iloc[i, 0],
                                           avg_preparation_time=workbook.iloc[i, 4],
                                           note=workbook.iloc[i, 26])

        # menu_cat_obj, created = MenuCategory.objects.get_or_create(pk=int(workbook.iloc[i, 6]),
        #                                                            defaults={'title': workbook.iloc[i, 5],
        #                                                                      'weight': int(workbook.iloc[i, 27])})

        macro_product_obj, created = MacroProduct.objects.get_or_create(pk=int(workbook.iloc[i, 9]),
                                                                        defaults={'title': workbook.iloc[i, 8]})

        content_option_obj, created = ContentOption.objects.get_or_create(pk=int(workbook.iloc[i, 12]),
                                                                          defaults={'title': workbook.iloc[i, 11]})

        macro_product_content_obj, created = MacroProductContent.objects.get_or_create(pk=int(workbook.iloc[i, 15]),
                                                                                       defaults={'title': workbook.iloc[i, 14]})

        size_option_obj, created = SizeOption.objects.get_or_create(pk=int(workbook.iloc[i, 21]),
                                                                    defaults={'title': workbook.iloc[i, 20]})

        product_variant_obj, created = ProductVariant.objects.get_or_create(pk=int(workbook.iloc[i, 18]),
                                                                            defaults={'title': workbook.iloc[i, 17],
                                                                                      'menu_item': menu_obj,
                                                                                      'size_option': size_option_obj,
                                                                                      'macro_product_content': macro_product_content_obj})

        # menu_obj.category = menu_cat_obj
        menu_obj.title = workbook.iloc[i, 0]
        menu_obj.guid_1c = workbook.iloc[i, 3]
        menu_obj.save()

        macro_product_content_obj.content_option = content_option_obj
        macro_product_content_obj.macro_product = macro_product_obj
        macro_product_content_obj.save()

        product_variant_obj.menu_item = menu_obj
        product_variant_obj.size_option = size_option_obj
        product_variant_obj.macro_product_content = macro_product_content_obj
        product_variant_obj.save()

        print(workbook.iloc[i, 24])
        product_option_ids = workbook.iloc[i, 24].split()
        for product_option_id in product_option_ids:
            product_option_obj, created = ProductOption.objects.get_or_create(pk=int(product_option_id),
                                                                              defaults={'title': workbook.iloc[i, 23],
                                                                                        'menu_item': menu_obj})
            product_option_obj.product_variants.add(product_variant_obj)


    print('-----------------')
