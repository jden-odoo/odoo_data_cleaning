odoo.define('bsa_import.import', function(require){
    
    var BaseImport = require('base_import.import').DataImport;

    var core = require('web.core');

    var BSAImport = BaseImport.include({

        _handleMappingComments: function(changedField, fieldInfo) {
            // check if two columns are mapped on the same fields (for char/text fields)
            var commentsToAdd = [];
            var $sameMappedFields = this.$('.oe_import_comment_cell[field="' + fieldInfo.id + '"]');

            if (fieldInfo.type == 'many2many') {
                commentsToAdd.push(QWeb.render('ImportView.comment_m2m_field'));
            }
            if ($sameMappedFields.length >= 2) {
                if (['char', 'text', "many2many"].includes(fieldInfo.type)) {
                    commentsToAdd.push(QWeb.render('ImportView.comment_same_mapped_field', {
                        field: fieldInfo.text,
                    }));
                } else if (fieldInfo.id == 'child_column'){
                    return;
                }
                else {  // if column is mapped on an already mapped field, remove that field from the old column.
                    var $targetMappedFieldId = $(changedField).parent().find('div.oe_import_match_field').getAttributes()['id'];
                    _.each($sameMappedFields, function(fieldComment) {
                        var $mappingCell = $(fieldComment).parent().find('div.oe_import_match_field');
                        if ($mappingCell.getAttributes()['id'] !== $targetMappedFieldId) {
                            $mappingCell.find('.select2-search-choice-close').trigger('mousedown').trigger('click');
                        }
                    });
                }
            }

            var $commentDiv = $sameMappedFields.find(".oe_import_comments_div");
            $commentDiv.empty();
            _.each($commentDiv, function(fieldComment) {
                _.each(commentsToAdd, function(comment) {
                    $(fieldComment).append(comment);
                });
            });
        },

        render_fields_matches: function(result, $fields) {
            result.fields.unshift({
                fields: [],
                id: 'child_column',
                name: 'child_column',
                required: false,
                type: "id",
                string: "Child Column",
            })
            this._super.apply(this, arguments)
        },

        call_import: function(kwargs) {
            console.log('hi mom')
            var fields = this.$('input.oe_import_match_field').map(function (index, el) {
                return $(el).select2('val') || false;
            }).get();
            var columns = this.$('.o_import_header_name').map(function () {
                return $(this).text().trim().toLowerCase() || false;
            }).get();
            //TODO: raise error for missing info
            var user = this.$('#oe_user').val();
            var password = this.$('#oe_api_key').val();
            var db = this.$('#oe_db_name').val();
            var url = this.$('#oe_db_url').val();

            return this._rpc({
                model: 'base_import.import',
                method: 'execute_import',
                args: [this.id, user, password, db, url, fields, columns, 'product.template'],
            }, {
                shadow: true
            }).then(function(result) {
                // return Promise.resolve({'messages': [{
                //     type: 'error',
                //     record: false,
                //     message: msg,
                // }]})
                return Promise.resolve(({'messages': [{}]}));
            });



        }
    });

    return {DataImport: BSAImport}
})