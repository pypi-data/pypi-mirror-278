(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
    typeof define === 'function' && define.amd ? define(['exports'], factory) :
    (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global.Djblets = global.Djblets || {}));
})(this, (function (exports) { 'use strict';

    var _class$3;
    /**
     * Settings for the avatar configuration form.
     */



    /**
     * Attributes for the Settings model.
     *
     * Version Added:
     *     5.0
     */

    /**
     * Settings for the avatar configuration form.
     */
    let Settings = Spina.spina(_class$3 = class Settings extends Spina.BaseModel {
      /**
       * Return defaults for the model attributes.
       *
       * Returns:
       *     SettingsAttributes:
       *     Default values for the model attributes.
       */
      static defaults() {
        return {
          configuration: {},
          serviceID: null,
          services: {}
        };
      }
    }) || _class$3;

    function _defineProperty(obj, key, value) {
      if (key in obj) {
        Object.defineProperty(obj, key, {
          value: value,
          enumerable: true,
          configurable: true,
          writable: true
        });
      } else {
        obj[key] = value;
      }
      return obj;
    }
    function _classPrivateFieldGet(receiver, privateMap) {
      var descriptor = _classExtractFieldDescriptor(receiver, privateMap, "get");
      return _classApplyDescriptorGet(receiver, descriptor);
    }
    function _classPrivateFieldSet(receiver, privateMap, value) {
      var descriptor = _classExtractFieldDescriptor(receiver, privateMap, "set");
      _classApplyDescriptorSet(receiver, descriptor, value);
      return value;
    }
    function _classExtractFieldDescriptor(receiver, privateMap, action) {
      if (!privateMap.has(receiver)) {
        throw new TypeError("attempted to " + action + " private field on non-instance");
      }
      return privateMap.get(receiver);
    }
    function _classApplyDescriptorGet(receiver, descriptor) {
      if (descriptor.get) {
        return descriptor.get.call(receiver);
      }
      return descriptor.value;
    }
    function _classApplyDescriptorSet(receiver, descriptor, value) {
      if (descriptor.set) {
        descriptor.set.call(receiver, value);
      } else {
        if (!descriptor.writable) {
          throw new TypeError("attempted to set read only private field");
        }
        descriptor.value = value;
      }
    }
    function _checkPrivateRedeclaration(obj, privateCollection) {
      if (privateCollection.has(obj)) {
        throw new TypeError("Cannot initialize the same private elements twice on an object");
      }
    }
    function _classPrivateFieldInitSpec(obj, privateMap, value) {
      _checkPrivateRedeclaration(obj, privateMap);
      privateMap.set(obj, value);
    }

    var _class$2;
    /**
     * A base class for avatar service settings forms.
     */



    /**
     * A base class for avatar service settings forms.
     *
     * Subclasses should override this to provide additional behaviour for
     * previews, etc.
     */
    let ServiceSettingsFormView = Spina.spina(_class$2 = class ServiceSettingsFormView extends Spina.BaseView {
      /**
       * Validate the form.
       *
       * Returns:
       *     boolean:
       *     Whether or not the form is valid.
       */
      validate() {
        return true;
      }

      /**
       * Hide the form.
       *
       * This will set the disabled and hidden states.
       *
       * Version Changed:
       *     5.0:
       *     This no longer alters the ``display`` state of the element.
       *
       * Returns:
       *     ServiceSettingsFormView:
       *     This object, for chaining.
       */
      hide() {
        const el = this.el;
        el.disabled = true;
        el.hidden = true;
        return this;
      }

      /**
       * Show the form.
       *
       * This will remove the disabled and hidden states.
       *
       * Version Changed:
       *     5.0:
       *     This no longer alters the ``display`` state of the element.
       *
       * Returns:
       *     ServiceSettingsFormView:
       *     This object, for chaining.
       */
      show() {
        const el = this.el;
        el.disabled = false;
        el.hidden = false;
        return this;
      }
    }) || _class$2;

    var _class$1, _class2$1, _$box, _$preview, _$fileInput;
    const allowedMimeTypes = ['image/gif', 'image/jpeg', 'image/png'];

    /**
     * A file upload avatar settings form.
     *
     * This form provides a preview of the uploaded avatar.
     */
    let FileUploadSettingsFormView = Spina.spina(_class$1 = (_$box = /*#__PURE__*/new WeakMap(), _$preview = /*#__PURE__*/new WeakMap(), _$fileInput = /*#__PURE__*/new WeakMap(), (_class2$1 = class FileUploadSettingsFormView extends ServiceSettingsFormView {
      constructor() {
        super(...arguments);
        _classPrivateFieldInitSpec(this, _$box, {
          writable: true,
          value: void 0
        });
        _classPrivateFieldInitSpec(this, _$preview, {
          writable: true,
          value: void 0
        });
        _classPrivateFieldInitSpec(this, _$fileInput, {
          writable: true,
          value: void 0
        });
      }
      /**
       * Validate the form.
       *
       * If a file is selected, ensure it is has the correct MIME type.
       *
       * Returns:
       *     boolean:
       *     Whether the form is valid.
       */
      validate() {
        const file = _classPrivateFieldGet(this, _$fileInput)[0].files[0];
        if (!file) {
          alert(gettext("You must choose a file."));
          return false;
        }
        if (!allowedMimeTypes.some(el => el === file.type)) {
          alert(gettext("This wasn't a valid image file format. Please provide a PNG, JPEG, or GIF file."));
          return false;
        }
        return true;
      }

      /**
       * Render the form.
       */
      onInitialRender() {
        _classPrivateFieldSet(this, _$box, this.$('.avatar-file-upload-config'));
        _classPrivateFieldSet(this, _$preview, this.$('.avatar-preview'));
        _classPrivateFieldSet(this, _$fileInput, this.$('#id_file-upload-avatar_upload'));
      }

      /**
       * Handler for a click event on the "browse" instruction text.
       *
       * This will trigger opening the hidden file input.
       *
       * Args:
       *     e (jQuery.Event):
       *         The click event.
       */
      _onBrowseClicked(e) {
        e.preventDefault();
        e.stopPropagation();

        /*
         * Clicking on the file input itself is not reliable. There are ways
         * to make it work, but the browser actively avoids letting you do it
         * if it seems to be hidden. However, it works just fine universally to
         * click on the label.
         */
        this.$('#avatar-file-upload-browse-label').click();
      }

      /**
       * Handler for a drag enter event.
       *
       * If the configuration box is being hovered over, this will enable the
       * hover state, giving users an indication that they can drop the image
       * there.
       *
       * Args:
       *     e (jQuery.Event):
       *         The drag over event.
       */
      _onDragEnter(e) {
        e.preventDefault();
        e.stopPropagation();
        if (e.target === _classPrivateFieldGet(this, _$box)[0]) {
          _classPrivateFieldGet(this, _$box).width(_classPrivateFieldGet(this, _$box).width()).addClass('drag-hover');
        }
      }

      /**
       * Handler for a drag over event.
       *
       * If the configuration box is being hovered over, this will set the drop
       * effect.
       *
       * Args:
       *     e (jQuery.Event):
       *         The drag over event.
       */
      _onDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        if (e.target === _classPrivateFieldGet(this, _$box)[0]) {
          const dt = e.originalEvent.dataTransfer;
          if (dt) {
            dt.dropEffect = 'copy';
          }
        }
      }

      /**
       * Handler for a drag leave event.
       *
       * If the configuration box is being left, this will remove the hover state
       * and reset the drop effect.
       *
       * Args:
       *     e (jQuery.Event):
       *         The drag leave event.
       */
      _onDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        if (e.target === _classPrivateFieldGet(this, _$box)[0]) {
          _classPrivateFieldGet(this, _$box).removeClass('drag-hover').width('auto');
          const dt = e.originalEvent.dataTransfer;
          if (dt) {
            dt.dropEffect = 'none';
          }
        }
      }

      /**
       * Handler for a drop operation.
       *
       * This will remove the hover state and attempt to set the list of files
       * on the file input. If this fails (which will be the case on some
       * browsers with older behavior), the user will receive an alert telling
       * them it failed and to try browsing instead.
       *
       * If all goes well, the avatar will be ready for upload and the preview
       * image will be updated.
       *
       * Args:
       *     e (jQuery.Event):
       *         The drop event.
       */
      _onDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        _classPrivateFieldGet(this, _$box).removeClass('drag-hover');
        const dt = e.originalEvent.dataTransfer;
        const files = dt && dt.files;
        if (!files || files.length === 0) {
          return;
        }
        if (files.length > 1) {
          alert(gettext("You can only set one file as your avatar. Please drag and drop a single file."));
          return;
        }
        const fileType = files[0].type;
        if (fileType !== 'image/png' && fileType !== 'image/jpeg' && fileType !== 'image/gif') {
          alert(gettext("This doesn't appear to be a compatible image file for avatars. Please upload a PNG, JPEG, or GIF file."));
          return;
        }
        try {
          _classPrivateFieldGet(this, _$fileInput)[0].files = files;
        } catch (exc) {
          /*
           * While most modern browsers allow setting the `files` property of
           * an input field to the rest of a drag-and-drop operation, not all
           * do (I'm looking at you, IE/Edge). Older browsers will also
           * complain. So instead of outright failing, tell the user that
           * this won't work and suggest a workaround.
           */
          alert(gettext("Looks like dragging to upload a file isn't going to work with your browser. Try browsing for a file instead."));
          return;
        }
        this._setAvatarFromFile(files[0]);
      }

      /**
       * Handler for when the file input has changed.
       *
       * This will update the preview image.
       *
       * Args:
       *     e (jQuery.Event):
       *         The change event.
       */
      _onFileChanged(e) {
        const file = e.target.files[0];
        if (file) {
          this._setAvatarFromFile(file);
        }
      }

      /**
       * Set the avatar from the provided file upload.
       *
       * Args:
       *     file (File):
       *         The file that was uploaded.
       */
      _setAvatarFromFile(file) {
        const reader = new FileReader();
        reader.addEventListener('load', () => {
          _classPrivateFieldGet(this, _$preview).empty().removeClass('avatar-preview-unset').append($('<img>').attr({
            alt: gettext("Your new avatar"),
            src: reader.result
          }));
        });
        reader.readAsDataURL(file);
      }
    }, _defineProperty(_class2$1, "events", {
      'change #id_file-upload-avatar_upload': '_onFileChanged',
      'click .avatar-file-upload-browse': '_onBrowseClicked',
      'click .avatar-preview': '_onBrowseClicked',
      'dragenter .avatar-file-upload-config': '_onDragEnter',
      'dragleave .avatar-file-upload-config': '_onDragLeave',
      'dragover .avatar-file-upload-config': '_onDragOver',
      'drop .avatar-file-upload-config': '_onDrop'
    }), _class2$1))) || _class$1;

    var _class, _class2;
    /**
     * A form for managing the settings of avatar services.
     */


    let resolveReady;
    const readyPromise = new Promise((resolve, reject) => {
      resolveReady = resolve;
    });

    /**
     * A form for managing the settings of avatar services.
     *
     * This form lets you select the avatar service you wish to use, as well as
     * configure the settings for that avatar service.
     */
    let SettingsFormView = Spina.spina(_class = (_class2 = class SettingsFormView extends Spina.BaseView {
      /**
       * Add a configuration form to the instance.
       *
       * Args:
       *     serviceID (string):
       *         The unique ID for the avatar service.
       *
       *     formClass (constructor):
       *         The view to use for the form.
       */
      static addConfigForm(serviceID, formClass) {
        SettingsFormView.instance._configForms.set(serviceID, new formClass({
          el: $(`[data-avatar-service-id="${serviceID}"]`),
          model: SettingsFormView.instance.model
        }));
      }

      /**
       * Initialize the form.
       */
      initialize() {
        console.assert(SettingsFormView.instance === null);
        SettingsFormView.instance = this;
        this._configForms = new Map();
        this._$config = this.$('.avatar-service-configuration');
        this.listenTo(this.model, 'change:serviceID', () => this._showHideForms());

        /*
         * The promise continuations will only be executed once the stack is
         * unwound.
         */
        resolveReady();
      }

      /**
       * Validate the current form upon submission.
       *
       * Args:
       *     e (Event):
       *         The form submission event.
       */
      _onSubmit(e) {
        const serviceID = this.model.get('serviceID');
        const currentForm = this._configForms.get(serviceID);
        if (currentForm && !currentForm.validate()) {
          e.preventDefault();
        }
      }

      /**
       * Render the child forms.
       *
       * This will show the for the currently selected service if it has one.
       */
      renderForms() {
        for (const form of this._configForms.values()) {
          form.render();
        }

        /*
         * Ensure that if the browser sets the value of the <select> upon
         * refresh that we update the model accordingly.
         */
        this.$('#id_avatar_service_id').change();
        this._showHideForms();
      }

      /**
       * Show or hide the configuration form.
       */
      _showHideForms() {
        const serviceID = this.model.get('serviceID');
        const currentForm = this._configForms.get(serviceID);
        const previousID = this.model.previous('serviceID');
        const previousForm = previousID ? this._configForms.get(previousID) : undefined;
        if (previousForm && currentForm) {
          previousForm.hide();
          currentForm.show();
        } else if (previousForm) {
          previousForm.hide();
          this._$config.hide();
        } else if (currentForm) {
          currentForm.show();
          this._$config.show();
        }
      }

      /**
       * Handle the service being changed.
       *
       * Args:
       *     e (Event):
       *         The change event.
       */
      _onServiceChanged(e) {
        const $target = $(e.target);
        const serviceID = $target.val();
        this.model.set('serviceID', serviceID);
      }
    }, _defineProperty(_class2, "events", {
      'change #id_avatar_service_id': '_onServiceChanged',
      'submit': '_onSubmit'
    }), _defineProperty(_class2, "instance", null), _defineProperty(_class2, "ready", readyPromise), _class2)) || _class;

    /* Define a namespace for Djblets.Avatars. */
    const Avatars = {
      FileUploadSettingsFormView,
      ServiceSettingsFormView,
      Settings,
      SettingsFormView
    };

    exports.Avatars = Avatars;

}));
//# sourceMappingURL=index.js.map
