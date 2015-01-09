# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.category'
        db.add_column(u'products_product', 'category',
                      self.gf('django.db.models.fields.CharField')(default='tops', max_length=120),
                      keep_default=False)

        # Adding field 'ProductImage.description'
        db.add_column(u'products_productimage', 'description',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ProductImage.size'
        db.add_column(u'products_productimage', 'size',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ProductImage.front'
        db.add_column(u'products_productimage', 'front',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ProductImage.back'
        db.add_column(u'products_productimage', 'back',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ProductImage.detail'
        db.add_column(u'products_productimage', 'detail',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.category'
        db.delete_column(u'products_product', 'category')

        # Deleting field 'ProductImage.description'
        db.delete_column(u'products_productimage', 'description')

        # Deleting field 'ProductImage.size'
        db.delete_column(u'products_productimage', 'size')

        # Deleting field 'ProductImage.front'
        db.delete_column(u'products_productimage', 'front')

        # Deleting field 'ProductImage.back'
        db.delete_column(u'products_productimage', 'back')

        # Deleting field 'ProductImage.detail'
        db.delete_column(u'products_productimage', 'detail')


    models = {
        u'products.product': {
            'Meta': {'unique_together': "(('title', 'slug'),)", 'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'tops'", 'max_length': '120'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '29.99', 'max_digits': '100', 'decimal_places': '2'}),
            'sale_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '100', 'decimal_places': '2', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'products.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'back': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'detail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'front': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Product']"}),
            'size': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thumbnail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'products.variation': {
            'Meta': {'object_name': 'Variation'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'size'", 'max_length': '120'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ProductImage']", 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '100', 'decimal_places': '2', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Product']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['products']