from django.db import models

from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_update_time = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")
    is_active = models.BooleanField(default=True, verbose_name='是否有效')


class GoodsUnits(BaseModel):
    """
    商品单位
    """
    CAL_TYPE = (
        (0, 'kg'),
        (1, '个数'),
        (2, '公益回收')
    )
    name = models.CharField(max_length=20, verbose_name='分类名', unique=True)
    cal_type = models.IntegerField(choices=CAL_TYPE, null=True, verbose_name='颜色')
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, verbose_name='单位价格')
    # pic_url = models.CharField(max_length=100, null=True, verbose_name='图片链接地址')
    order = models.IntegerField(null=True, verbose_name='排序id')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '回收品价格'
        verbose_name_plural = verbose_name
        db_table = 'production'


class ProductClassify(BaseModel):
    """
    首页商品分类信息
    """

    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
    )
    type_title = models.CharField('类型名称', max_length=20)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)  # 是否删除,默认不删
    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    # 设置目录树的级别
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="父类目级别", related_name="sub_cat")

    def __str__(self):
        return self.type_title

    class Meta:
        verbose_name = '分类信息'
        verbose_name_plural = '分类信息'


class Goods(BaseModel):
    """
    商品
    """
    category = models.ForeignKey(ProductClassify, verbose_name="所属分类", on_delete=models.CASCADE,
                                 related_name="category_product_classify")
    goods_sn = models.CharField(verbose_name="商品唯一货号", max_length=50, default="", )
    name = models.CharField(verbose_name="商品名", max_length=100, )
    click_num = models.IntegerField(verbose_name="点击数", default=0, )
    sold_num = models.IntegerField(verbose_name="销量", default=0, )
    fav_num = models.IntegerField(verbose_name="收藏数", default=0, )
    goods_num = models.IntegerField(verbose_name="库存数", default=0, )
    market_price = models.FloatField(verbose_name="市场价格", default=0, )
    shop_price = models.FloatField(verbose_name="本店价格", default=0, )
    goods_brief = models.TextField(verbose_name="描述", max_length=500, )
    is_new = models.BooleanField(verbose_name="是否新品", default=False, )  # 首页中新品展示
    ship_free = models.BooleanField(verbose_name="是否承担运费", default=True, )
    # 首页中展示的商品封面图
    goods_front_image = models.ImageField(verbose_name="封面图", upload_to="goods/images/", null=True, blank=True, )
    # 商品详情页的热卖商品，自行设置
    is_hot = models.BooleanField(verbose_name="是否热销", default=False, )

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(BaseModel):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品", related_name="images")
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)

    class Meta:
        verbose_name = '商品轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(BaseModel):
    """
    首页轮播的商品图
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")

    class Meta:
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class OrderHistory(BaseModel):
    '''
    订单记录
    '''
    WAY = (
        (1, '微信'),
        (2, '支付宝'),
        (3, '银行卡')
    )
    STATUS = (
        (1, '待付款'),
        (2, '付款中'),
        (3, '已付款'),
    )
    TYPE = (
        (1, '未发货'),
        (1, '运输中'),
        (2, '已收货'),
    )

    delivery_date = models.DateTimeField(verbose_name='发货日期')
    receipt_date = models.DateTimeField(verbose_name='收获日期')
    order_time = models.DateTimeField(verbose_name='下单时间')
    trade_no = models.CharField(max_length=100, verbose_name='交易号')
    quantity_ordered = models.IntegerField(verbose_name="下单数量", default=1, )
    real_quantity = models.IntegerField(verbose_name="实际数量", default=1, )
    actual_amount_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='实际付款金额', default=0.00)
    payment_method = models.IntegerField(choices=WAY, verbose_name='付款方式')
    payment_status = models.IntegerField(choices=STATUS, verbose_name='付款状态')
    time_of_payment = models.DateTimeField(verbose_name='付款时间')
    shipping_status = models.IntegerField(choices=TYPE, verbose_name='发货状态')
