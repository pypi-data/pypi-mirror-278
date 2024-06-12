(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
  typeof define === 'function' && define.amd ? define(['exports'], factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global.Djblets = global.Djblets || {}));
})(this, (function (exports) { 'use strict';

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
  function _classPrivateMethodGet(receiver, privateSet, fn) {
    if (!privateSet.has(receiver)) {
      throw new TypeError("attempted to get private field on non-instance");
    }
    return fn;
  }
  function _checkPrivateRedeclaration(obj, privateCollection) {
    if (privateCollection.has(obj)) {
      throw new TypeError("Cannot initialize the same private elements twice on an object");
    }
  }
  function _classPrivateMethodInitSpec(obj, privateSet) {
    _checkPrivateRedeclaration(obj, privateSet);
    privateSet.add(obj);
  }

  var _class$1, _class2$1, _class3$1, _class4$1, _class5$1, _class6$1;
  /**
   * Extension management support.
   */





  /**
   * Attributes for information on an installed extension.
   *
   * Version Added:
   *     4.0
   */
  /**
   * Represents an installed extension listed in the Manage Extensions list.
   *
   * This stores the various information about the extension that we'll display
   * to the user, and offers actions for enabling or disabling the extension.
   */
  let InstalledExtension = Spina.spina(_class$1 = (_class2$1 = class InstalledExtension extends Spina.BaseModel {
    /**
     * Enable the extension.
     *
     * This will submit a request to the server to enable this extension.
     *
     * Returns:
     *     Promise:
     *     A promise that will be resolved when the request to enable the
     *     extension completes.
     */
    enable() {
      return new Promise((resolve, reject) => {
        this.save({
          enabled: true
        }, {
          wait: true,
          error: (model, xhr) => {
            this.set({
              canEnable: !xhr.errorRsp.needs_reload,
              loadError: xhr.errorRsp.load_error,
              loadable: false
            });
            reject(new Error(xhr.errorText));
          },
          success: () => resolve()
        });
      });
    }

    /**
     * Disable the extension.
     *
     * This will submit a request to the server to disable this extension.
     *
     * Returns:
     *     Promise:
     *     A promise that will be resolved when the request to enable the
     *     extension completes.
     */
    disable() {
      return new Promise((resolve, reject) => {
        this.save({
          enabled: false
        }, {
          wait: true,
          error: xhr => reject(new Error(xhr.errorText)),
          success: () => resolve()
        });
      });
    }

    /**
     * Return a JSON payload for requests sent to the server.
     *
     * Returns:
     *     object:
     *     A payload that will be serialized for making the API request.
     */
    toJSON() {
      return {
        enabled: this.get('enabled')
      };
    }

    /**
     * Parse a JSON payload from the server.
     *
     * Args:
     *     rsp (object):
     *         The payload from the server.
     *
     * Returns:
     *     object:
     *     The parsed response.
     */
    parse(rsp) {
      if (rsp.stat !== undefined) {
        rsp = rsp.extension;
      }
      const id = rsp.class_name;
      const configLink = rsp.links['admin-configure'];
      const dbLink = rsp.links['admin-database'];
      this.url = `${this.collection.url}${id}/`;
      return {
        author: rsp.author,
        authorURL: rsp.author_url,
        canDisable: rsp.can_disable,
        canEnable: rsp.can_enable,
        configURL: configLink ? configLink.href : null,
        dbURL: dbLink ? dbLink.href : null,
        enabled: rsp.enabled,
        id: id,
        loadError: rsp.load_error,
        loadable: rsp.loadable,
        name: rsp.name,
        summary: rsp.summary,
        version: rsp.version
      };
    }

    /**
     * Perform AJAX requests against the server-side API.
     *
     * Args:
     *     method (string):
     *         The HTTP method to use.
     *
     *     model (InstalledExtension):
     *         The extension object being synced.
     *
     *     options (object):
     *         Options for the sync operation.
     */
    sync(method, model, options) {
      return Backbone.sync.call(this, method, model, _.defaults({
        contentType: 'application/x-www-form-urlencoded',
        data: model.toJSON(),
        processData: true,
        error: (xhr, textStatus, errorThrown) => {
          let rsp;
          let text;
          try {
            rsp = $.parseJSON(xhr.responseText);
            text = rsp.err.msg;
          } catch (e) {
            text = 'HTTP ' + xhr.status + ' ' + xhr.statusText;
            rsp = {
              canEnable: false,
              loadError: text
            };
          }
          if (_.isFunction(options.error)) {
            xhr.errorText = text;
            xhr.errorRsp = rsp;
            options.error(xhr, textStatus, errorThrown);
          }
        }
      }, options));
    }
  }, _defineProperty(_class2$1, "defaults", {
    author: null,
    authorURL: null,
    configURL: null,
    dbURL: null,
    enabled: false,
    loadError: null,
    loadable: true,
    name: null,
    summary: null,
    version: null
  }), _class2$1)) || _class$1;
  /**
   * A collection of installed extensions.
   *
   * This stores the list of installed extensions, and allows fetching from
   * the API.
   */
  let InstalledExtensionCollection = Spina.spina(_class3$1 = (_class4$1 = class InstalledExtensionCollection extends Spina.BaseCollection {
    /**
     * Parse the response from the server.
     *
     * Args:
     *     rsp (object):
     *         The response from the server.
     *
     * Returns:
     *     object:
     *     The parsed data from the response.
     */
    parse(rsp) {
      return rsp.extensions;
    }
  }, _defineProperty(_class4$1, "model", InstalledExtension), _class4$1)) || _class3$1;
  /**
   * Manages installed extensions.
   *
   * This stores a collection of installed extensions, and provides
   * functionality for loading the current list from the server.
   */
  let ExtensionManager = Spina.spina(_class5$1 = (_class6$1 = class ExtensionManager extends Spina.BaseModel {
    /**
     * Initialize the manager.
     */
    initialize() {
      this.installedExtensions = new InstalledExtensionCollection();
      this.installedExtensions.url = this.get('apiRoot');
    }

    /**
     * Load the extensions list.
     */
    load() {
      this.trigger('loading');
      this.installedExtensions.fetch({
        success: () => this.trigger('loaded')
      });
    }
  }, _defineProperty(_class6$1, "defaults", {
    apiRoot: null
  }), _class6$1)) || _class5$1;

  var _class, _class2, _updateActions, _updateItemState, _class3, _class4, _class5, _class6;
  /**
   * Displays the interface showing all installed extensions.
   */




  /**
   * An item in the list of registered extensions.
   *
   * This will contain information on the extension and actions for toggling
   * the enabled state, reloading the extension, or configuring the extension.
   */
  let ExtensionItem = Spina.spina(_class = (_updateActions = /*#__PURE__*/new WeakSet(), _updateItemState = /*#__PURE__*/new WeakSet(), (_class2 = class ExtensionItem extends Djblets.ConfigFormsListItem {
    constructor() {
      super(...arguments);
      _classPrivateMethodInitSpec(this, _updateItemState);
      _classPrivateMethodInitSpec(this, _updateActions);
    }
    /**
     * Initialize the item.
     *
     * This will set up the initial state and then listen for any changes
     * to the extension's state (caused by enabling/disabling/reloading the
     * extension).
     *
     * Args:
     *     attributes (ListItemConstructorAttrs, optional):
     *         Attributes for the model.
     */
    initialize() {
      let attributes = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      super.initialize(attributes);
      _classPrivateMethodGet(this, _updateActions, _updateActions2).call(this);
      _classPrivateMethodGet(this, _updateItemState, _updateItemState2).call(this);
      this.listenTo(this.get('extension'), 'change:loadable change:loadError change:enabled', () => {
        _classPrivateMethodGet(this, _updateItemState, _updateItemState2).call(this);
        _classPrivateMethodGet(this, _updateActions, _updateActions2).call(this);
      });
    }

    /**
     * Update the actions for the extension.
     *
     * If the extension is disabled, this will add an Enabled action.
     *
     * If it's enabled, but has a load error, it will add a Reload action.
     *
     * If it's enabled, it will provide actions for Configure and Database,
     * if enabled by the extension, along with a Disable action.
     */
  }, _defineProperty(_class2, "defaults", {
    extension: null
  }), _class2))) || _class;
  /**
   * Displays an extension in the Manage Extensions list.
   *
   * This will show information about the extension, and provide links for
   * enabling/disabling the extension, and (depending on the extension's
   * capabilities) configuring it or viewing its database.
   */
  function _updateActions2() {
    const extension = this.get('extension');
    const actions = [];
    if (!extension.get('loadable')) {
      /* Add an action for reloading the extension. */
      actions.push({
        id: 'reload',
        label: gettext("Reload")
      });
    } else if (extension.get('enabled')) {
      /*
       * Show all the actions for enabled extensions.
       *
       * Note that the order used is here to ensure visual alignment
       * for most-frequently-used options.
       */
      const configURL = extension.get('configURL');
      const dbURL = extension.get('dbURL');
      if (dbURL) {
        actions.push({
          id: 'database',
          label: gettext("Database"),
          url: dbURL
        });
      }
      if (configURL) {
        actions.push({
          id: 'configure',
          label: gettext("Configure"),
          primary: true,
          url: configURL
        });
      }
      actions.push({
        danger: true,
        id: 'disable',
        label: gettext("Disable")
      });
    } else {
      /* Add an action for enabling a disabled extension. */
      actions.push({
        id: 'enable',
        label: gettext("Enable"),
        primary: true
      });
    }
    this.setActions(actions);
  }
  function _updateItemState2() {
    const extension = this.get('extension');
    let itemState;
    if (!extension.get('loadable')) {
      itemState = 'error';
    } else if (extension.get('enabled')) {
      itemState = 'enabled';
    } else {
      itemState = 'disabled';
    }
    this.set('itemState', itemState);
  }
  let ExtensionItemView = Spina.spina(_class3 = (_class4 = class ExtensionItemView extends Djblets.ConfigFormsTableItemView {
    /**
     * Return context data for rendering the item's template.
     *
     * Returns:
     *     object:
     *     Context data for the render.
     */
    getRenderContext() {
      return this.model.get('extension').attributes;
    }

    /**
     * Handle a click on the Disable action.
     *
     * This will make an asynchronous request to disable the extension.
     *
     * Returns:
     *     Promise:
     *     A promise for the disable request. This will resolve once the
     *     API has handled the request.
     */
    _onDisableClicked() {
      return this.model.get('extension').disable().catch(error => {
        alert(interpolate(gettext("Failed to disable the extension: %(value1)s."), {
          "value1": error.message
        }, true));
      });
    }

    /**
     * Handle a click on the Enable action.
     *
     * This will make an asynchronous request to enable the extension.
     *
     * Returns:
     *     Promise:
     *     A promise for the enable request. This will resolve once the
     *     API has handled the request.
     */
    _onEnableClicked() {
      return this.model.get('extension').enable().catch(error => {
        alert(interpolate(gettext("Failed to enable the extension: %(value1)s."), {
          "value1": error.message
        }, true));
      });
    }

    /**
     * Handle a click on the Reload action.
     *
     * This will trigger an event on the item that tells the extension
     * manager to perform a full reload of all extensions, this one included.
     *
     * Returns:
     *     Promise:
     *     A promise for the enable request. This will never resolve, in
     *     practice, but is returned to enable the action's spinner until
     *     the page reloads.
     */
    _onReloadClicked() {
      return new Promise(() => this.model.trigger('needsReload'));
    }
  }, _defineProperty(_class4, "className", 'djblets-c-extension-item djblets-c-config-forms-list__item'), _defineProperty(_class4, "actionHandlers", {
    'disable': '_onDisableClicked',
    'enable': '_onEnableClicked',
    'reload': '_onReloadClicked'
  }), _defineProperty(_class4, "template", _.template(`<td class="djblets-c-config-forms-list__item-main">
 <div class="djblets-c-extension-item__header">
  <h3 class="djblets-c-extension-item__name"><%- name %></h3>
  <span class="djblets-c-extension-item__version"><%- version %></span>
  <div class="djblets-c-extension-item__author">
   <% if (authorURL) { %>
    <a href="<%- authorURL %>"><%- author %></a>
   <% } else { %>
    <%- author %>
   <% } %>
  </div>
 </div>
 <p class="djblets-c-extension-item__description">
  <%- summary %>
 </p>
 <% if (!loadable) { %>
  <pre class="djblets-c-extension-item__load-error"><%-
    loadError %></pre>
 <% } %>
</td>
<td class="djblets-c-config-forms-list__item-state"></td>
<td></td>`)), _class4)) || _class3;
  /**
   * Displays the interface showing all installed extensions.
   *
   * This loads the list of installed extensions and displays each in a list.
   */
  let ExtensionManagerView = Spina.spina(_class5 = (_class6 = class ExtensionManagerView extends Spina.BaseView {
    /**
     * Initialize the view.
     */
    initialize() {
      this.list = new Djblets.ConfigFormsList({}, {
        collection: new Djblets.ConfigFormsListItems([], {
          model: ExtensionItem
        })
      });
    }

    /**
     * Render the view.
     */
    onInitialRender() {
      const model = this.model;
      const list = this.list;
      this.listView = new Djblets.ConfigFormsTableView({
        ItemView: ExtensionItemView,
        el: this.$('.djblets-c-config-forms-list'),
        model: list
      });
      this.listView.render().$el.removeAttr('aria-busy').addClass('-all-items-are-multiline');
      this.listenTo(model, 'loading', () => list.collection.reset());
      this.listenTo(model, 'loaded', this._onLoaded);
      model.load();
    }

    /**
     * Handler for when the list of extensions is loaded.
     *
     * Renders each extension in the list. If the list is empty, this will
     * display that there are no extensions installed.
     */
    _onLoaded() {
      const items = this.list.collection;
      this.model.installedExtensions.each(extension => {
        const item = items.add({
          extension: extension
        });
        this.listenTo(item, 'needsReload', this._reloadFull);
      });
    }

    /**
     * Perform a full reload of the list of extensions on the server.
     *
     * This submits our form, which is set in the template to tell the
     * ExtensionManager to do a full reload.
     */
    _reloadFull() {
      this.el.submit();
    }
  }, _defineProperty(_class6, "events", {
    'click .djblets-c-extensions__reload': '_reloadFull'
  }), _class6)) || _class5;

  exports.ExtensionManager = ExtensionManager;
  exports.ExtensionManagerView = ExtensionManagerView;

}));
//# sourceMappingURL=index.js.map
