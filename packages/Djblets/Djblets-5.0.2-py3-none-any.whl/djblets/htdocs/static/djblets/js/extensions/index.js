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

  var _class$2, _class2$1;
  /**
   * Base class for an extension.
   */


  /**
   * Base class for an extension.
   *
   * Extensions that deal with JavaScript should subclass this to provide any
   * initialization code it needs, such as the initialization of hooks.
   *
   * Extension instances will have read access to the server-stored settings
   * for the extension.
   */
  let Extension = Spina.spina(_class$2 = (_class2$1 = class Extension extends Spina.BaseModel {
    /**
     * Initialize the extension.
     *
     * Subclasses that override this are expected to call this method.
     */
    initialize() {
      this.hooks = [];
    }
  }, _defineProperty(_class2$1, "defaults", {
    id: null,
    name: null,
    settings: {}
  }), _class2$1)) || _class$2;

  var _dec, _class$1, _class2;
  /**
   * Base support for defining extension hooks.
   */


  /**
   * Base class for hooks that an extension can use to augment functionality.
   *
   * Each type of hook represents a point in the codebase that an extension
   * is able to plug functionality into.
   *
   * Subclasses are expected to set a hookPoint field in the prototype to an
   * instance of ExtensionPoint.
   *
   * Instances of an ExtensionHook subclass that extensions create will be
   * automatically registered with both the extension and the list of hooks
   * for that ExtensionHook subclass.
   *
   * Callers that use ExtensionHook subclasses to provide functionality can
   * use the subclass's each() method to loop over all registered hooks.
   */
  let ExtensionHook = (_dec = Spina.spina({
    prototypeAttrs: ['each', 'hookPoint']
  }), _dec(_class$1 = (_class2 = class ExtensionHook extends Spina.BaseModel {
    /**
     * An ExtensionHookPoint instance.
     *
     * This must be defined and instantiated by a subclass of ExtensionHook,
     * but not by subclasses created by extensions.
     */

    /**
     * Loop through each registered hook instance and call the given callback.
     *
     * Args:
     *     cb (function):
     *         The callback to call.
     *
     *     context (object, optional):
     *         Optional context to use when calling the callback.
     */
    static each(cb) {
      let context = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
      for (const hook of this.prototype.hookPoint.hooks) {
        cb.call(context, hook);
      }
    }

    /**
     * Initialize the hook.
     *
     * This will add the instance of the hook to the extension's list of
     * hooks, and to the list of known hook instances for this hook point.
     *
     * After initialization, setUpHook will be called, which a subclass
     * can use to provide additional setup.
     */
    initialize() {
      const extension = this.get('extension');
      console.assert(!!this.hookPoint, 'This ExtensionHook subclass must define hookPoint');
      console.assert(!!extension, 'An Extension instance must be passed to ExtensionHook');
      extension.hooks.push(this);
      this.hookPoint.addHook(this);
      this.setUpHook();
    }

    /**
     * Set up additional state for the hook.
     *
     * This can be overridden by subclasses to provide additional
     * functionality.
     */
    setUpHook() {
      /* Empty by default. */
    }
  }, _defineProperty(_class2, "hookPoint", null), _defineProperty(_class2, "defaults", {
    extension: null
  }), _class2)) || _class$1);

  var _class;
  /**
   * Class for defining a hook point for extension hooks.
   */


  /**
   * Defines a point where extension hooks can plug into.
   *
   * This is meant to be instantiated and provided as a 'hookPoint' field on
   * an ExtensionHook subclass, in order to provide a place to hook into.
   */
  let ExtensionHookPoint = Spina.spina(_class = class ExtensionHookPoint extends Spina.BaseModel {
    /**********************
     * Instance variables *
     **********************/

    /**
     * A list of all hooks registered on this extension point.
     */

    /**
     * Initialize the hook point.
     */
    initialize() {
      this.hooks = [];
    }

    /**
     * Add a hook instance to the list of known hooks.
     *
     * Args:
     *     hook (Djblets.ExtensionHook):
     *         The hook instance.
     */
    addHook(hook) {
      this.hooks.push(hook);
    }
  }) || _class;

  exports.Extension = Extension;
  exports.ExtensionHook = ExtensionHook;
  exports.ExtensionHookPoint = ExtensionHookPoint;

}));
//# sourceMappingURL=index.js.map
