from django import template
from django.utils.safestring import mark_safe

from products.models import *

register = template.Library()

TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """

PRODUCT_SPEC = {
    'notebook': {
        'Діагональ дисплея': 'display',
        'Тип накопичувача': 'rom',
        'Об\'єм пам\'яті, Гб': 'rom_capacity',
        'Тип оперативної пам\'яті': 'ram',
        'Об\'єм оперативної пам\'яті, Гб': 'rom_capacity',
        'Час автономної роботи, години': 'battery_lifetime',
        'Ємніть батареї, Ват-г': 'battery_capacity',
    },
    'tablet': {
        'Діагональ дисплея': 'display',
        'Об\'єм пам\'яті, Гб': 'rom_capacity',
        'Об\'єм оперативної пам\'яті, Гб': 'rom_capacity',
        'Наявність фронтальної камери': 'is_front_cam',
        'Фронтальна камера, МП': 'front_cam',
        'Наявність задня камери': 'is_back_cam',
        'Задня камера, МП': 'back_cam',
        'Підтримка SD карт': 'is_sd',
        'Максимальний обсяг пам\'яті, Гб': 'sd',
        'Час автономної роботи, години': 'battery_lifetime',
        'Ємніть батареї, мАг': 'battery_capacity',
    },
    'personalcomputer': {
        'Тип накопичувача': 'rom',
        'Об\'єм пам\'яті, Гб': 'rom_capacity',
        'Тип оперативної пам\'яті': 'ram',
        'Об\'єм оперативної пам\'яті, Гб': 'rom_capacity',
    },
    'smartphone': {
        'Діагональ дисплея': 'display',
        'Об\'єм пам\'яті': 'rom_capacity',
        'Об\'єм оперативної пам\'яті': 'rom_capacity',
        'Наявність фронтальної камери': 'is_front_cam',
        'Фронтальна камера': 'front_cam',
        'Наявність задня камери': 'is_back_cam',
        'Задня камера': 'back_cam',
        'Підтримка SD карт': 'is_sd',
        'Максимальний обсяг пам\'яті, Гб': 'sd',
        'Час автономної роботи, години': 'battery_lifetime',
        'Ємніть батареї, мАг': 'battery_capacity',
    },
    'tvset': {
        'Діагональ дисплея': 'display',
        'Формат екрану': 'ds_type',
        'Роздільна здатність екрану': 'ds_resolution',
    },
    'audio': {
        'Тип': 'audio_type',
        'Тип підключення': 'connect_type',
        'Мінімальна частота навушника, Гц': 'min_sound_freq',
        'Максимальна частота навушника, Гц': 'max_sound_freq',
    },
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)

