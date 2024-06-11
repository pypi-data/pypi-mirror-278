odoo.define('sm_connect.FormControllerConfirmation', function (require) {
    "use strict";
    var Dialog = require('web.Dialog');
    var viewRegistry = require('web.view_registry');
    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var form_controller_confirmation = FormController.extend({
        _onSave: function (ev) {
            ev.stopPropagation(); // Prevent x2m lines to be auto-saved
            // wait for potential pending changes to be saved (done with widgets
            // allowing to edit in readonly)
            var self = this;

            var confirmDialog = new Dialog(self, {
                title: _t("Confirmación"),
                size: 'medium',
                $content: $("<div><p>Dado el estado actual del vehículo tus cambios se enviarán a Fleetio</p><p>¿Estás seguro de guardar?</p></div>"),
                buttons: [{
                    text: _t("Ok"),
                    classes: 'btn-primary',
                    click: function () {
                        self._disableButtons();
                        self.saveRecord().always(function () {
                            self._enableButtons();
                        });
                        confirmDialog.close();
                    }
                }, {
                    text: _t("Cancelar"),
                    classes: 'btn-secondary',
                    click: function () {
                        confirmDialog.close();
                    }
                }]
            });
            if(this.model.localData[this.handle].data.maintenance || (this.model.localData[this.handle]._changes && "maintenance" in this.model.localData[this.handle]._changes)) {
                confirmDialog.open();
            } else{
                self._disableButtons();
                self.saveRecord().always(function () {
                    self._enableButtons();
                });
                confirmDialog.close();
            }
        },
    });

    var form_view_confirmation = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: form_controller_confirmation,
        }),
    });

    viewRegistry.add('form_confirmation', form_view_confirmation);
    return form_controller_confirmation;
});





