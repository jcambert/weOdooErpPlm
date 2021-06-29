odoo.define('mrp.plm.plm_kanban', function (require) {
    'use strict';

    var KanbanController = require('web.KanbanController');
    var KanbanView = require('web.KanbanView');
    var view_registry = require('web.view_registry');
    var KanbanRecord = require('web.KanbanRecord');

    KanbanRecord.include({
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @override
         * @private
         */
        // YTI TODO: Should be transformed into a extend and specific to project
        _openRecord: function () {
            if (this.selectionMode !== true && this.modelName === 'mrp.plm' &&
                this.$(".oe_plm_kanban_global_click>a:first-child").length) {
                this.$('.oe_plm_kanban_global_click>a:first-child').first().click();
            } else {
                this._super.apply(this, arguments);
            }
        },
    });

    var PlmKanbanController = KanbanController.extend({});

    var PlmKanbanView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Controller: PlmKanbanController
        }),
    });



    view_registry.add('plm_kanban', PlmKanbanView);

    return PlmKanbanController;
});
