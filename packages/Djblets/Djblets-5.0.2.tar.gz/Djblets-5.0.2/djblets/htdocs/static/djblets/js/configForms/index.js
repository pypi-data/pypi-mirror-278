(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
  typeof define === 'function' && define.amd ? define(['exports'], factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global.Djblets = global.Djblets || {}));
})(this, (function (exports) { 'use strict';

  var _class$7;
  /**
   * Base class for a list used for config forms.
   */



  /**
   * Base class for a list used for config forms.
   */
  let List = Spina.spina(_class$7 = class List extends Spina.BaseModel {}) || _class$7;

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
  function _classPrivateFieldInitSpec(obj, privateMap, value) {
    _checkPrivateRedeclaration(obj, privateMap);
    privateMap.set(obj, value);
  }
  function _classPrivateMethodInitSpec(obj, privateSet) {
    _checkPrivateRedeclaration(obj, privateSet);
    privateSet.add(obj);
  }

  var _class$6, _class2$4;
  /**
   * Base class for an item in a list for config forms.
   */



  /**
   * Attributes for the ListItem model.
   *
   * Version Added:
   *     4.0
   */

  /**
   * Base class for an item in a list for config forms.
   *
   * ListItems provide text representing the item, optionally linked. They
   * can also provide zero or more actions that can be invoked on the item
   * by the user.
   */
  let ListItem = Spina.spina(_class$6 = (_class2$4 = class ListItem extends Spina.BaseModel {
    constructor() {
      super(...arguments);
      _defineProperty(this, "actions", []);
      _defineProperty(this, "itemStateTexts", {
        disabled: gettext("Disabled"),
        enabled: gettext("Enabled"),
        error: gettext("Error")
      });
    }
    /**
     * Initialize the item.
     *
     * If showRemove is true, this will populate a default Remove action
     * for removing the item.
     *
     * Args:
     *     attributes (ListItemAttrs, optional):
     *         Attributes for the model.
     */
    initialize() {
      let attributes = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      console.assert(attributes.actions === undefined, `Passing in actions to the Djblets.Config.ListItem constructor
has been removed as of Djblets 5.0. Actions should be passed
to the setActions() method instead.`);
      if (this.get('showRemove')) {
        this.actions.push({
          danger: true,
          enabled: this.get('canRemove'),
          id: 'delete',
          label: this.get('removeLabel')
        });
      }
    }

    /**
     * Set the actions available for this item.
     *
     * Args:
     *     actions (Array of ListItemAction):
     *         The new action definitions.
     */
    setActions(actions) {
      this.actions = actions;
      this.trigger('actionsChanged');
    }
  }, _defineProperty(_class2$4, "defaults", {
    canRemove: true,
    editURL: null,
    itemState: null,
    loading: false,
    removeLabel: gettext("Remove"),
    showRemove: false,
    text: null
  }), _class2$4)) || _class$6;

  var _dec$2, _class$5, _class2$3, _$itemState;
  /**
   * Base view for displaying a list item in config pages.
   */


  /**
   * Base view for displaying a list item in config pages.
   *
   * The list item will show information on the item and any actions that can
   * be invoked.
   *
   * By default, this will show the text from the ListItem model, linking it
   * if the model has an editURL attribute. This can be customized by subclasses
   * by overriding ``template``.
   */
  let ListItemView = (_dec$2 = Spina.spina({
    prototypeAttrs: ['actionHandlers', 'iconBaseClassName', 'itemStateClasses', 'template']
  }), _dec$2(_class$5 = (_$itemState = /*#__PURE__*/new WeakMap(), (_class2$3 = class ListItemView extends Spina.BaseView {
    constructor() {
      super(...arguments);
      _classPrivateFieldInitSpec(this, _$itemState, {
        writable: true,
        value: void 0
      });
    }
    /**
     * Initialize the view.
     */
    initialize() {
      this.listenTo(this.model, 'actionsChanged', this.render);
      this.listenTo(this.model, 'request', this.showSpinner);
      this.listenTo(this.model, 'sync', this.hideSpinner);
      this.listenTo(this.model, 'destroy', this.remove);
      this.$spinnerParent = null;
      this.$spinner = null;
    }

    /**
     * Render the view.
     *
     * This will be called every time the list of actions change for
     * the item.
     */
    onRender() {
      const model = this.model;
      this.$el.empty().append(this.template(_.defaults(model.attributes, this.getRenderContext())));
      _classPrivateFieldSet(this, _$itemState, this.$('.djblets-c-config-forms-list__item-state'));
      this.listenTo(model, 'change:itemState', this._onItemStateChanged);
      this._onItemStateChanged();
      this.addActions(this.getActionsParent());
    }

    /**
     * Return additional render context.
     *
     * By default this returns an empty object. Subclasses can use this to
     * provide additional values to :js:attr:`template` when it is rendered.
     *
     * Returns:
     *     ListItemViewRenderContext:
     *     Additional rendering context for the template.
     */
    getRenderContext() {
      return {};
    }

    /**
     * Remove the item.
     *
     * This will fade out the item, and then remove it from view.
     */
    remove() {
      this.$el.fadeOut('normal', () => super.remove());
      return this;
    }

    /**
     * Return the container for the actions.
     *
     * This defaults to being this element, but it can be overridden to
     * return a more specific element.
     *
     * Returns:
     *     jQuery:
     *     The container for the actions.
     */
    getActionsParent() {
      return this.$el;
    }

    /**
     * Display a spinner on the item.
     *
     * This can be used to show that the item is being loaded from the
     * server.
     */
    showSpinner() {
      if (this.$spinner) {
        return;
      }
      this.$el.attr('aria-busy', 'true');
      this.$spinner = $('<span>').addClass('djblets-o-spinner').attr('aria-hidden', 'true').prependTo(this.$spinnerParent).hide().css('visibility', 'visible').fadeIn();
    }

    /**
     * Hide the currently visible spinner.
     */
    hideSpinner() {
      if (!this.$spinner) {
        return;
      }

      /*
       * The slow fadeout does two things:
       *
       * 1) It prevents the spinner from disappearing too quickly
       *    (in combination with the fadeIn above), in case the operation
       *    is really fast, giving some feedback that something actually
       *    happened.
       *
       * 2) By fading out, it doesn't look like it just simply stops.
       *    Helps provide a sense of completion.
       */
      this.$spinner.fadeOut('slow', () => {
        this.$spinner.remove();
        this.$spinner = null;
      });
      this.$el.removeAttr('aria-busy');
    }

    /**
     * Add all registered actions to the view.
     *
     * Args:
     *     $parentEl (jQuery):
     *         The parent element to add the actions to.
     */
    addActions($parentEl) {
      const $actions = $('<span>').addClass('djblets-c-config-forms-list__item-actions');
      this.model.actions.forEach(action => {
        const $action = this._buildActionEl(action).appendTo($actions);
        if (action.children) {
          if (action.label) {
            $action.append(' &#9662;');
          }

          /*
           * Show the dropdown after we let this event propagate.
           */
          $action.click(() => _.defer(() => this._showActionDropdown(action, $action)));
        }
      });
      this.$spinnerParent = $actions;
      $actions.prependTo($parentEl);
    }

    /**
     * Show a dropdown for a menu action.
     *
     * Args:
     *     action (object):
     *         The action to show the dropdown for. See
     *         :js:class:`Djblets.Config.ListItem`. for a list of attributes.
     *
     *     $action (jQuery):
     *         The element that represents the action.
     */
    _showActionDropdown(action, $action) {
      const actionPos = $action.position();
      const $menu = $('<div>').css({
        minWidth: $action.outerWidth(),
        position: 'absolute'
      }).addClass('djblets-c-config-forms-popup-menu').click(e => e.stopPropagation());
      const $items = $('<ul>').addClass('djblets-c-config-forms-popup-menu__items').appendTo($menu);
      const actionLeft = actionPos.left + $action.getExtents('m', 'l');
      action.children.forEach(childAction => $('<li>').addClass('djblets-c-config-forms-popup-menu__item ' + `config-forms-list-action-row-${childAction.id}`).append(this._buildActionEl(childAction)).appendTo($items));
      this.trigger('actionMenuPopUp', {
        $action: $action,
        $menu: $menu,
        action: action
      });
      $menu.appendTo($action.parent());
      const winWidth = $(window).width();
      const paneWidth = $menu.width();
      $menu.move($action.offset().left + paneWidth > winWidth ? actionLeft + $action.innerWidth() - paneWidth : actionLeft, actionPos.top + $action.outerHeight(), 'absolute');

      /* Any click outside this dropdown should close it. */
      $(document).one('click', () => {
        this.trigger('actionMenuPopDown', {
          $action: $action,
          $menu: $menu,
          action: action
        });
        $menu.remove();
      });
    }

    /**
     * Build the element for an action.
     *
     * If the action's type is ``'checkbox'``, a checkbox will be shown.
     * Otherwise, the action will be shown as a button.
     *
     * Args:
     *     action (ListItemAction):
     *         The action to show the dropdown for. See
     *         :js:class:`Djblets.Config.ListItem` for a list of attributes.
     */
    _buildActionEl(action) {
      const enabled = action.enabled !== false;
      const actionHandlerName = enabled ? this.actionHandlers[action.id] : null;
      const isCheckbox = action.type === 'checkbox';
      const isRadio = action.type === 'radio';
      let $action;
      let $result;
      if (isCheckbox || isRadio) {
        const inputID = _.uniqueId('action_' + action.type);
        $action = $('<input>').attr({
          id: inputID,
          name: action.name,
          type: action.type
        });
        const $label = $('<label>').attr('for', inputID).text(action.label);
        if (action.id) {
          $label.addClass(`config-forms-list-action-label-${action.id}`);
        }
        $result = $('<span>').append($action).append($label);
        if (action.propName) {
          if (isCheckbox) {
            $action.bindProperty('checked', this.model, action.propName);
          } else if (isRadio) {
            $action.bindProperty('checked', this.model, action.propName, {
              radioValue: action.radioValue
            });
          }
        }
        if (action.enabledPropName) {
          $action.bindProperty('disabled', this.model, action.enabledPropName, {
            inverse: action.enabledPropInverse !== true
          });
        }
        if (actionHandlerName) {
          const actionHandler = _.debounce(this[actionHandlerName].bind(this), 50, true);
          $action.change(actionHandler);
          if (isRadio && action.dispatchOnClick) {
            $action.click(actionHandler);
          }
        }
      } else {
        if (action.url) {
          $action = $('<a class="ink-c-button" role="button">').attr('href', action.url);
        } else {
          $action = $('<button class="ink-c-button" type="button">');
        }
        $result = $action;
        if (action.label) {
          $action.text(action.label);
        }
        if (action.ariaLabel) {
          $action.attr('aria-label', action.ariaLabel);
        }
        if (action.iconName) {
          $action.prepend($('<span>').addClass(this.iconBaseClassName).addClass(`${this.iconBaseClassName}-${action.iconName}`));
        }
        if (actionHandlerName) {
          $action.click(evt => {
            evt.preventDefault();
            evt.stopPropagation();
            this._onActionButtonClicked(evt, actionHandlerName, $action);
          });
        }
      }
      $action.addClass('djblets-c-config-forms-list__item-action');
      if (action.id) {
        $action.addClass(`config-forms-list-action-${action.id}`);
      }
      if (action.danger) {
        $action.addClass('-is-danger');
      }
      if (action.primary) {
        $action.addClass('-is-primary');
      }
      if (!enabled) {
        $action.prop('disabled', true);
      }
      return $result;
    }

    /**
     * Handle changes to the item state.
     *
     * This will update the CSS class used on the item and any relevant text
     * contained within the item to reflect the current state.
     */
    _onItemStateChanged() {
      const model = this.model;
      const oldItemState = model.previous('itemState');
      const itemState = model.get('itemState');
      if (oldItemState) {
        this.$el.removeClass(this.itemStateClasses[oldItemState]);
      }
      if (itemState) {
        this.$el.addClass(this.itemStateClasses[itemState]);

        /*
         * Note that if we didn't find an element in the template for
         * this before, this is basically a no-op.
         */
        _classPrivateFieldGet(this, _$itemState).text(model.itemStateTexts[itemState]);
      }
    }

    /**
     * Handle clicks on a list item action button.
     *
     * This will invoke the click handler on the view. If that handler
     * returns a Promise, this will disable the button, replace its contents
     * with a spinner, and then wait for the promise to resolve before
     * setting the button's contents and enabled states back to normal.
     *
     * Args:
     *     evt (jQuery.Event):
     *         The click event on the button.
     *
     *     actionHandlerName (string):
     *         The name of the action handler function to call.
     *
     *     $action (jQuery):
     *         The action button that was clicked.
     */
    _onActionButtonClicked(evt, actionHandlerName, $action) {
      const promise = this[actionHandlerName].call(this, evt);
      if (promise && typeof promise.then === 'function') {
        $action.prop('disabled', true);
        const childrenHTML = $action.html();
        $action.empty();
        const $spinner = $('<span class="ink-c-spinner">').appendTo($action);

        /*
         * This is a promise, so there's an async operation
         * going on. Set up the spinner.
         */
        promise.finally(() => {
          $spinner.remove();
          $action.html(childrenHTML);
          $action.prop('disabled', false);
        });
      }
    }
  }, _defineProperty(_class2$3, "className", 'djblets-c-config-forms-list__item'), _defineProperty(_class2$3, "tagName", 'li'), _defineProperty(_class2$3, "iconBaseClassName", 'djblets-icon'), _defineProperty(_class2$3, "itemStateClasses", {
    disabled: '-is-disabled',
    enabled: '-is-enabled',
    error: '-has-error'
  }), _defineProperty(_class2$3, "template", _.template(`<% if (editURL) { %>
<a href="<%- editURL %>"><%- text %></a>
<% } else { %>
<%- text %>
<% } %>`)), _defineProperty(_class2$3, "actionHandlers", {}), _class2$3))) || _class$5);

  var _class$4;
  /**
   * Base class for a collection of ListItems.
   */



  /**
   * Base class for a collection of ListItems.
   *
   * This operates just like a standard :js:class:`Backbone.Collection`, with two
   * additions:
   *
   * 1. It stores the provided options, for later usage, preventing subclasses
   *    from having to provide their own initialize function.
   *
   * 2. It emits a "fetching" event when calling :js:meth:`fetch`, allowing views
   *    to provide a visual indication when items are being fetched or rendered.
   */
  let ListItems = Spina.spina(_class$4 = class ListItems extends Spina.BaseCollection {
    /**********************
     * Instance variables *
     **********************/

    /** The saved options. */

    /**
     * Initialize the collection.
     *
     * Args:
     *     models (array):
     *         The models to add to the collection.
     *
     *     options (object):
     *         Options for the collection.
     */
    initialize(models, options) {
      this.options = options;
    }

    /**
     * Fetch the contents of the collection.
     *
     * This will emit the ``fetching`` event, and then call
     * Backbone.Collection's fetch().
     *
     * Args:
     *     options (object):
     *         Options to pass to the base class's ``fetch`` method.
     */
    fetch(options) {
      this.trigger('fetching');
      return super.fetch(options);
    }
  }) || _class$4;

  var _dec$1, _class$3, _class2$2, _renderItems;

  /**
   * Options for the ListView.
   *
   * Version Added:
   *     4.0
   */

  /**
   * View for displaying a list of items.
   *
   * This will render each item in a list, and update that list when the
   * items in the collection changes.
   *
   * It can also filter the displayed list of items.
   *
   * If loading the list through the API, this will display a loading indicator
   * until the items have been loaded.
   *
   * If 'options.animateItems' is true, then newly added or removed items will
   * be faded in/out.
   */
  let ListView = (_dec$1 = Spina.spina({
    prototypeAttrs: ['defaultItemView']
  }), _dec$1(_class$3 = (_renderItems = /*#__PURE__*/new WeakSet(), (_class2$2 = class ListView extends Spina.BaseView {
    constructor() {
      super(...arguments);
      _classPrivateMethodInitSpec(this, _renderItems);
      _defineProperty(this, "$listBody", null);
    }
    /**
     * Initialize the view.
     *
     * Args:
     *     options (object, optional):
     *         The view options.
     *
     * Option Args:
     *     ItemView (object):
     *         The item view class to use. This argument defaults to
     *         :js:attr:`defaultItemView`.
     *
     *     animateItems (boolean):
     *         Whether or not items should be animated. This argument
     *         defaults to ``false``.
     */
    initialize() {
      let options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
      const collection = this.model.collection;
      this.ItemView = options.ItemView || this.defaultItemView;
      this.views = [];
      this.animateItems = !!options.animateItems;
      this.once('rendered', () => {
        this.listenTo(collection, 'add', this.addItem);
        this.listenTo(collection, 'remove', this.removeItem);
        this.listenTo(collection, 'reset', _classPrivateMethodGet(this, _renderItems, _renderItems2));
      });
    }

    /**
     * Return the body element.
     *
     * This can be overridden by subclasses if the list items should be
     * rendered to a child element of this view.
     *
     * Returns:
     *     jQuery:
     *     Where the list view should be rendered.
     */
    getBody() {
      return this.$el;
    }

    /**
     * Render the list of items.
     *
     * This will loop through all items and render each one.
     */
    onRender() {
      this.$listBody = this.getBody();
      _classPrivateMethodGet(this, _renderItems, _renderItems2).call(this);
      this.trigger('rendered');
    }

    /**
     * Create a view for an item and adds it.
     *
     * Args:
     *     item (Backbone.Model):
     *         The model to add.
     *
     *     collection (Backbone.Collection):
     *         Ignored.
     *
     *     options (AddRemoveOptions, optional):
     *         Options for adding the item.
     */
    addItem(item, collection) {
      let options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
      const animateItem = options.animate !== false;
      const view = new this.ItemView({
        model: item
      });
      view.render();

      /*
       * If this ListView has animation enabled, and this specific
       * item is being animated (the default unless options.animate
       * is false), we'll fade in the item.
       */
      if (this.animateItems && animateItem) {
        view.$el.fadeIn();
      }
      this.$listBody.append(view.$el);
      this.views.push(view);
    }

    /**
     * Handle an item being removed from the collection.
     *
     * Removes the element from the list.
     *
     * Args:
     *     item (Backbone.Model):
     *         The model to remove.
     *
     *     collection (Backbone.Collection):
     *         Ignored.
     *
     *     options (object, optional):
     *         Options for removing the element.
     *
     * Option Args:
     *     animate (boolean):
     *         Whether or not the removal should be animated. This defaults
     *         to ``true``.
     */
    removeItem(item, collection) {
      let options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
      const animateItem = options.animate !== false;
      const view = _.find(this.views, view => view.model === item);
      if (view) {
        this.views = _.without(this.views, view);

        /*
         * If this ListView has animation enabled, and this specific
         * item is being animated (the default unless options.animate
         * is false), we'll fade out the item.
         */
        if (this.animateItems && animateItem) {
          view.$el.fadeOut(function () {
            view.remove();
          });
        } else {
          view.remove();
        }
      }
    }

    /**
     * Render all items from the list.
     */
  }, _defineProperty(_class2$2, "className", 'djblets-c-config-forms-list'), _defineProperty(_class2$2, "tagName", 'ul'), _defineProperty(_class2$2, "defaultItemView", ListItemView), _class2$2))) || _class$3);
  function _renderItems2() {
    this.views.forEach(view => view.remove());
    this.views = [];
    this.$listBody.empty();
    this.model.collection.each(item => {
      this.addItem(item, item.collection, {
        animate: false
      });
    });
  }

  var _class$2, _$activeNav, _$activePage, _preserveMessages;
  /**
   * View to manage a collection of configuration pages.
   */




  /**
   * View to manage a collection of configuration pages.
   *
   * The primary job of this view is to handle sub-page navigation.
   * The actual page will contain several "pages" that are shown or hidden
   * depending on what the user has clicked on the sidebar.
   */
  let PagesView = Spina.spina(_class$2 = (_$activeNav = /*#__PURE__*/new WeakMap(), _$activePage = /*#__PURE__*/new WeakMap(), _preserveMessages = /*#__PURE__*/new WeakMap(), class PagesView extends Spina.BaseView {
    constructor() {
      super(...arguments);
      _classPrivateFieldInitSpec(this, _$activeNav, {
        writable: true,
        value: void 0
      });
      _classPrivateFieldInitSpec(this, _$activePage, {
        writable: true,
        value: void 0
      });
      _classPrivateFieldInitSpec(this, _preserveMessages, {
        writable: true,
        value: void 0
      });
    }
    /**
     * Initialize the view.
     *
     * This will set up the router for handling page navigation.
     */
    initialize() {
      this.router = new Backbone.Router({
        routes: {
          ':pageID': 'page'
        }
      });
      this.listenTo(this.router, 'route:page', this._onPageChanged);
      _classPrivateFieldSet(this, _$activeNav, null);
      _classPrivateFieldSet(this, _$activePage, null);
      _classPrivateFieldSet(this, _preserveMessages, true);
    }

    /**
     * Render the view.
     *
     * This will set the default page to be shown, and instruct Backbone
     * to begin handling the routing.
     */
    onInitialRender() {
      this._$pageNavs = this.$('.djblets-c-config-forms-page-nav__item');
      this._$pages = this.$('.djblets-c-config-forms-subpage');
      _classPrivateFieldSet(this, _$activeNav, this._$pageNavs.eq(0).addClass('-is-active'));
      _classPrivateFieldSet(this, _$activePage, this._$pages.eq(0).addClass('-is-active'));
      Backbone.history.start({
        root: window.location.pathname
      });
    }

    /**
     * Handle when the page changes.
     *
     * The sidebar will be updated to reflect the current active page,
     * and the page will be shown.
     *
     * If navigating pages manually, any messages provided by the backend
     * form will be removed. We don't do this the first time there's a
     * navigation, as this will be called when first rendering the view.
     *
     * Args:
     *     pageID (string):
     *         The ID of the page that is becoming active.
     */
    _onPageChanged(pageID) {
      _classPrivateFieldGet(this, _$activeNav).removeClass('-is-active');
      _classPrivateFieldGet(this, _$activePage).removeClass('-is-active');
      _classPrivateFieldSet(this, _$activePage, $(`#page_${pageID}`));
      if (_classPrivateFieldGet(this, _$activePage).length === 0) {
        /*
         * If the requested page doesn't exist (for example, it might be
         * hidden, or just typoed), load the first page instead.
         */
        this.router.navigate(this._$pageNavs.find('a').attr('href').substr(1), {
          replace: true,
          trigger: true
        });
      } else {
        _classPrivateFieldSet(this, _$activeNav, this._$pageNavs.filter(`:has(a[href="#${pageID}"])`).addClass('-is-active'));
        _classPrivateFieldGet(this, _$activePage).addClass('-is-active');
        if (!_classPrivateFieldGet(this, _preserveMessages)) {
          $('#messages').remove();
        }
        _classPrivateFieldSet(this, _preserveMessages, false);
      }
    }
  })) || _class$2;

  var _class$1, _class2$1;

  /**
   * View to render a ListItem as a row in a table.
   *
   * This is meant to be used with TableView. Subclasses will generally want
   * to override the template.
   */
  let TableItemView = Spina.spina(_class$1 = (_class2$1 = class TableItemView extends ListItemView {
    /**
     * Return the container for the actions.
     *
     * This defaults to being the last cell in the row, but this can be
     * overridden to provide a specific cell or an element within.
     *
     * Returns:
     *     jQuery:
     *     The element where actions should be rendered.
     */
    getActionsParent() {
      return this.$('td:last');
    }
  }, _defineProperty(_class2$1, "tagName", 'tr'), _defineProperty(_class2$1, "template", _.template(`<td>
<% if (editURL) { %>
<a href="<%- editURL %>"><%- text %></a>
<% } else { %>
<%- text %>
<% } %>
</td>`)), _class2$1)) || _class$1;

  var _dec, _class, _class2;

  /**
   * A table-based view for a list of items.
   *
   * This is an extension to ListView that's designed for lists with multiple
   * columns of data.
   */
  let TableView = (_dec = Spina.spina({
    prototypeAttrs: ['defaultItemView']
  }), _dec(_class = (_class2 = class TableView extends ListView {
    /**
     * Render the view.
     *
     * If the element does not already have a <tbody>, one will be added.
     * All items will go under this.
     */
    onInitialRender() {
      const $body = this.getBody();
      if ($body.length === 0) {
        this.$el.append('<tbody>');
      }
      super.onInitialRender();
    }

    /**
     * Return the body element where items will be added.
     *
     * Returns:
     *     jQuery:
     *     The element where the items will be rendered.
     */
    getBody() {
      return this.$('tbody');
    }
  }, _defineProperty(_class2, "tagName", 'table'), _defineProperty(_class2, "defaultItemView", TableItemView), _class2)) || _class);

  const Config = {
    List,
    ListItem,
    ListItemView,
    ListItems,
    ListView,
    PagesView,
    TableItemView,
    TableView
  };

  exports.Config = Config;
  exports.ConfigFormsList = List;
  exports.ConfigFormsListItem = ListItem;
  exports.ConfigFormsListItemView = ListItemView;
  exports.ConfigFormsListItems = ListItems;
  exports.ConfigFormsListView = ListView;
  exports.ConfigFormsPagesView = PagesView;
  exports.ConfigFormsTableItemView = TableItemView;
  exports.ConfigFormsTableView = TableView;

}));
//# sourceMappingURL=index.js.map
