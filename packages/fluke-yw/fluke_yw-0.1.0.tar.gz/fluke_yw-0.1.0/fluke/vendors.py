
vendors = {
    "bootstrap": {
        'js': {
            'dev': 'fluke/vendor/bootstrap/js/bootstrap.js',
            'production': 'fluke/vendor/bootstrap/js/bootstrap.min.js',
            'cdn': 'http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js'
        },
        'css': {
            'dev': 'fluke/vendor/bootstrap/css/bootstrap.css',
            'production': 'fluke/vendor/bootstrap/css/bootstrap.css',
            'cdn': 'http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css'
        },
        'responsive': {'css':{
                'dev': 'fluke/vendor/bootstrap/bootstrap-responsive.css',
                'production': 'fluke/vendor/bootstrap/bootstrap-responsive.css'
            }}
    },
    'jquery': {
        "js": {
            'dev': 'fluke/vendor/jquery/jquery.js',
            'production': 'fluke/vendor/jquery/jquery.min.js',
        }
    },
    'jquery-ui-effect': {
        "js": {
            'dev': 'fluke/vendor/jquery-ui/jquery.ui.effect.js',
            'production': 'fluke/vendor/jquery-ui/jquery.ui.effect.min.js'
        }
    },
    'jquery-ui-sortable': {
        "js": {
            'dev': ['fluke/vendor/jquery-ui/jquery.ui.core.js', 'fluke/vendor/jquery-ui/jquery.ui.widget.js',
                    'fluke/vendor/jquery-ui/jquery.ui.mouse.js', 'fluke/vendor/jquery-ui/jquery.ui.sortable.js'],
            'production': ['fluke/vendor/jquery-ui/jquery.ui.core.min.js', 'fluke/vendor/jquery-ui/jquery.ui.widget.min.js',
                           'fluke/vendor/jquery-ui/jquery.ui.mouse.min.js', 'fluke/vendor/jquery-ui/jquery.ui.sortable.min.js']
        }
    },
    "font-awesome": {
        "css": {
            'dev': 'fluke/vendor/font-awesome/css/font-awesome.css',
            'production': 'fluke/vendor/font-awesome/css/font-awesome.min.css',
        }
    },
    "timepicker": {
        "css": {
            'dev': 'fluke/vendor/bootstrap-timepicker/css/bootstrap-timepicker.css',
            'production': 'fluke/vendor/bootstrap-timepicker/css/bootstrap-timepicker.min.css',
        },
        "js": {
            'dev': 'fluke/vendor/bootstrap-timepicker/js/bootstrap-timepicker.js',
            'production': 'fluke/vendor/bootstrap-timepicker/js/bootstrap-timepicker.min.js',
        }
    },
    "clockpicker": {
        "css": {
            'dev': 'fluke/vendor/bootstrap-clockpicker/bootstrap-clockpicker.css',
            'production': 'fluke/vendor/bootstrap-clockpicker/bootstrap-clockpicker.min.css',
        },
        "js": {
            'dev': 'fluke/vendor/bootstrap-clockpicker/bootstrap-clockpicker.js',
            'production': 'fluke/vendor/bootstrap-clockpicker/bootstrap-clockpicker.min.js',
        }
    },
    "datepicker": {
        "css": {
            'dev': 'fluke/vendor/bootstrap-datepicker/css/datepicker.css'
        },
        "js": {
            'dev': 'fluke/vendor/bootstrap-datepicker/js/bootstrap-datepicker.js',
        }
    },
    "flot": {
        "js": {
            'dev': ['fluke/vendor/flot/jquery.flot.js', 'fluke/vendor/flot/jquery.flot.pie.js', 'fluke/vendor/flot/jquery.flot.time.js',
                    'fluke/vendor/flot/jquery.flot.resize.js','fluke/vendor/flot/jquery.flot.aggregate.js','fluke/vendor/flot/jquery.flot.categories.js']
        }
    },
    "image-gallery": {
        "css": {
            'dev': 'fluke/vendor/bootstrap-image-gallery/css/bootstrap-image-gallery.css',
            'production': 'fluke/vendor/bootstrap-image-gallery/css/bootstrap-image-gallery.css',
        },
        "js": {
            'dev': ['fluke/vendor/load-image/load-image.js', 'fluke/vendor/bootstrap-image-gallery/js/bootstrap-image-gallery.js'],
            'production': ['fluke/vendor/load-image/load-image.min.js', 'fluke/vendor/bootstrap-image-gallery/js/bootstrap-image-gallery.js']
        }
    },
    "select": {
        "css": {
            'dev': ['fluke/vendor/select2/select2.css', 'fluke/vendor/selectize/selectize.css', 'fluke/vendor/selectize/selectize.bootstrap3.css'],
        },
        "js": {
            'dev': ['fluke/vendor/selectize/selectize.js', 'fluke/vendor/select2/select2.js', 'fluke/vendor/select2/select2_locale_%(lang)s.js'],
            'production': ['fluke/vendor/selectize/selectize.min.js', 'fluke/vendor/select2/select2.min.js', 'fluke/vendor/select2/select2_locale_%(lang)s.js']
        }
    },
    "multiselect": {
        "css": {
            'dev': 'fluke/vendor/bootstrap-multiselect/css/bootstrap-multiselect.css',
        },
        "js": {
            'dev': 'fluke/vendor/bootstrap-multiselect/js/bootstrap-multiselect.js',
        }
    },
    "snapjs": {
        "css": {
            'dev': 'fluke/vendor/snapjs/snap.css',
        },
        "js": {
            'dev': 'fluke/vendor/snapjs/snap.js',
        }
    },
}
