(function (factory) {
    typeof define === 'function' && define.amd ? define(factory) :
    factory();
})((function () { 'use strict';

    suite('djblets/configForms/models/ListItem', () => {
      window.describe('Default actions', () => {
        window.describe('showRemove', () => {
          window.it('true', () => {
            const listItem = new Djblets.ConfigFormsListItem({
              showRemove: true
            });
            window.expect(listItem.actions.length).toBe(1);
            window.expect(listItem.actions[0].id).toBe('delete');
          });
          window.it('false', () => {
            const listItem = new Djblets.ConfigFormsListItem({
              showRemove: false
            });
            window.expect(listItem.actions.length).toBe(0);
          });
        });
      });
    });

    window.suite('djblets/configForms/views/ListItemView', function () {
      window.describe('Rendering', function () {
        window.describe('General item display', function () {
          window.it('With editURL', function () {
            const item = new Djblets.ConfigFormsListItem({
              editURL: 'http://example.com/',
              text: 'Label'
            });
            const itemView = new Djblets.ConfigFormsListItemView({
              model: item
            });
            itemView.render();
            window.expect(itemView.$el.html().trim()).toBe(['<span class="djblets-c-config-forms-list__item-actions">', '</span>\n', '<a href="http://example.com/">Label</a>'].join(''));
          });
          window.it('Without editURL', function () {
            const item = new Djblets.ConfigFormsListItem({
              text: 'Label'
            });
            const itemView = new Djblets.ConfigFormsListItemView({
              model: item
            });
            itemView.render();
            window.expect(itemView.$el.html().trim()).toBe(['<span class="djblets-c-config-forms-list__item-actions">', '</span>\n', 'Label'].join(''));
          });
        });
        window.describe('Item states', function () {
          const CustomItemView = Djblets.ConfigFormsListItemView.extend({
            template: _.template(`<div><%- text %></div>
<div class="djblets-c-config-forms-list__item-state">
</div>`)
          });
          window.it('Initial render', function () {
            const item = new Djblets.ConfigFormsListItem({
              itemState: 'enabled'
            });
            const itemView = new CustomItemView({
              model: item
            });
            itemView.render();
            window.expect(itemView.el).toHaveClass('-is-enabled');
            const $stateText = itemView.$('.djblets-c-config-forms-list__item-state');
            window.expect($stateText.text()).toBe('Enabled');
          });
          window.it('When changed', function () {
            const item = new Djblets.ConfigFormsListItem({
              itemState: 'enabled'
            });
            const itemView = new CustomItemView({
              model: item
            });
            itemView.render();
            item.set('itemState', 'disabled');
            window.expect(itemView.el).toHaveClass('-is-disabled');
            window.expect(itemView.el).not.toHaveClass('-is-enabled');
            const $stateText = itemView.$('.djblets-c-config-forms-list__item-state');
            window.expect($stateText.text()).toBe('Disabled');
          });
        });
        window.describe('Actions', function () {
          window.it('Checkboxes', function () {
            const item = new Djblets.ConfigFormsListItem({
              checkboxAttr: false,
              text: 'Label'
            });
            item.setActions([{
              id: 'mycheckbox',
              label: 'Checkbox',
              propName: 'checkboxAttr',
              type: 'checkbox'
            }]);
            const itemView = new Djblets.ConfigFormsListItemView({
              model: item
            });
            itemView.render();
            window.expect(itemView.$('input[type=checkbox]').length).toBe(1);
            window.expect(itemView.$('label').length).toBe(1);
          });
          window.describe('Buttons', function () {
            window.it('Simple', function () {
              const item = new Djblets.ConfigFormsListItem({
                text: 'Label'
              });
              item.setActions([{
                id: 'mybutton',
                label: 'Button'
              }]);
              const itemView = new Djblets.ConfigFormsListItemView({
                model: item
              });
              itemView.render();
              const $button = itemView.$('button.djblets-c-config-forms-list__item-action');
              window.expect($button.length).toBe(1);
              const buttonEl = $button[0];
              window.expect($button.text()).toBe('Button');
              window.expect(buttonEl).toHaveClass('config-forms-list-action-mybutton');
              window.expect(buttonEl).not.toHaveClass('rb-icon');
              window.expect(buttonEl).not.toHaveClass('-is-danger');
              window.expect(buttonEl).not.toHaveClass('-is-primary');
            });
            window.it('Danger', function () {
              const item = new Djblets.ConfigFormsListItem({
                text: 'Label'
              });
              item.setActions([{
                danger: true,
                id: 'mybutton',
                label: 'Button'
              }]);
              const itemView = new Djblets.ConfigFormsListItemView({
                model: item
              });
              itemView.render();
              const $button = itemView.$('button.djblets-c-config-forms-list__item-action');
              window.expect($button.length).toBe(1);
              const buttonEl = $button[0];
              window.expect($button.text()).toBe('Button');
              window.expect(buttonEl).toHaveClass('config-forms-list-action-mybutton');
              window.expect(buttonEl).not.toHaveClass('rb-icon');
              window.expect(buttonEl).not.toHaveClass('-is-primary');
              window.expect(buttonEl).toHaveClass('-is-danger');
            });
            window.it('Primary', function () {
              const item = new Djblets.ConfigFormsListItem({
                text: 'Label'
              });
              item.setActions([{
                id: 'mybutton',
                label: 'Button',
                primary: true
              }]);
              const itemView = new Djblets.ConfigFormsListItemView({
                model: item
              });
              itemView.render();
              const $button = itemView.$('button.djblets-c-config-forms-list__item-action');
              window.expect($button.length).toBe(1);
              const buttonEl = $button[0];
              window.expect($button.text()).toBe('Button');
              window.expect(buttonEl).toHaveClass('config-forms-list-action-mybutton');
              window.expect(buttonEl).not.toHaveClass('rb-icon');
              window.expect(buttonEl).not.toHaveClass('-is-danger');
              window.expect(buttonEl).toHaveClass('-is-primary');
            });
            window.it('Icon names', function () {
              const item = new Djblets.ConfigFormsListItem({
                text: 'Label'
              });
              item.setActions([{
                danger: false,
                iconName: 'foo',
                id: 'mybutton',
                label: 'Button'
              }]);
              const itemView = new Djblets.ConfigFormsListItemView({
                model: item
              });
              itemView.render();
              const $button = itemView.$('button.djblets-c-config-forms-list__item-action');
              window.expect($button.length).toBe(1);
              const buttonEl = $button[0];
              window.expect($button.text()).toBe('Button');
              window.expect(buttonEl).toHaveClass('config-forms-list-action-mybutton');
              window.expect(buttonEl).not.toHaveClass('-is-danger');
              window.expect(buttonEl).not.toHaveClass('-is-primary');
              const $span = $button.find('span');
              window.expect($span.length).toBe(1);
              window.expect($span.hasClass('djblets-icon')).toBe(true);
              window.expect($span.hasClass('djblets-icon-foo')).toBe(true);
            });
          });
          window.describe('Menus', function () {
            let item;
            let itemView;
            window.beforeEach(function () {
              item = new Djblets.ConfigFormsListItem({
                text: 'Label'
              });
              item.setActions([{
                children: [{
                  id: 'mymenuitem',
                  label: 'My menu item'
                }],
                id: 'mymenu',
                label: 'Menu'
              }]);
              itemView = new Djblets.ConfigFormsListItemView({
                model: item
              });
              itemView.render();
            });
            window.it('Initial display', function () {
              const $button = itemView.$('button.djblets-c-config-forms-list__item-action');
              window.expect($button.length).toBe(1);
              window.expect($button.text()).toBe('Menu ▾');
            });
            window.it('Opening', function () {
              /* Prevent deferring. */
              window.spyOn(_, 'defer').and.callFake(function (cb) {
                cb();
              });
              window.spyOn(itemView, 'trigger');
              const $action = itemView.$('.config-forms-list-action-mymenu');
              $action.click();
              const $menu = itemView.$('.djblets-c-config-forms-popup-menu');
              window.expect($menu.length).toBe(1);
              window.expect(itemView.trigger.calls.mostRecent().args[0]).toBe('actionMenuPopUp');
            });
            window.it('Closing', function () {
              /* Prevent deferring. */
              window.spyOn(_, 'defer').and.callFake(cb => cb());
              const $action = itemView.$('.config-forms-list-action-mymenu');
              $action.click();
              window.spyOn(itemView, 'trigger');
              $(document.body).click();
              window.expect(itemView.trigger.calls.mostRecent().args[0]).toBe('actionMenuPopDown');
              const $menu = itemView.$('.action-menu');
              window.expect($menu.length).toBe(0);
            });
          });
          window.it('After render', () => {
            const item = new Djblets.ConfigFormsListItem({
              text: 'Label'
            });
            const itemView = new Djblets.ConfigFormsListItemView({
              model: item
            });
            itemView.render();
            let $button = itemView.$('button.djblets-c-config-forms-list__item-action');
            window.expect($button.length).toBe(0);

            /* Now set the actions. */
            item.setActions([{
              id: 'mybutton',
              label: 'Button'
            }]);
            $button = itemView.$('button.djblets-c-config-forms-list__item-action');
            window.expect($button.length).toBe(1);
            const buttonEl = $button[0];
            window.expect($button.text()).toBe('Button');
            window.expect(buttonEl).toHaveClass('config-forms-list-action-mybutton');
            window.expect(buttonEl).not.toHaveClass('rb-icon');
            window.expect(buttonEl).not.toHaveClass('-is-danger');
            window.expect(buttonEl).not.toHaveClass('-is-primary');
          });
        });
        window.describe('Action properties', function () {
          window.describe('enabledPropName', function () {
            window.it('value == undefined', function () {
              const item = new Djblets.ConfigFormsListItem({
                text: 'Label'
              });
              item.setActions([{
                enabledPropName: 'isEnabled',
                id: 'mycheckbox',
                label: 'Checkbox',
                type: 'checkbox'
              }]);
              const itemView = new Djblets.ConfigFormsListItemView({
                model: item
              });
              itemView.render();
              const $action = itemView.$('.config-forms-list-action-mycheckbox');
              window.expect($action.prop('disabled')).toBe(true);
            });
            window.it('value == true', function () {
              const item = new Djblets.ConfigFormsListItem({
                isEnabled: true,
                text: 'Label'
              });
              item.setActions([{
                enabledPropName: 'isEnabled',
                id: 'mycheckbox',
                label: 'Checkbox',
                type: 'checkbox'
              }]);
              const itemView = new Djblets.ConfigFormsListItemView({
                model: item
              });
              itemView.render();
              const $action = itemView.$('.config-forms-list-action-mycheckbox');
              window.expect($action.prop('disabled')).toBe(false);
            });
            window.it('value == false', function () {
              const item = new Djblets.ConfigFormsListItem({
                isEnabled: false,
                text: 'Label'
              });
              item.setActions([{
                enabledPropName: 'isEnabled',
                id: 'mycheckbox',
                label: 'Checkbox',
                type: 'checkbox'
              }]);
              const itemView = new Djblets.ConfigFormsListItemView({
                model: item
              });
              itemView.render();
              const $action = itemView.$('.config-forms-list-action-mycheckbox');
              window.expect($action.prop('disabled')).toBe(true);
            });
            window.describe('with enabledPropInverse == true', function () {
              window.it('value == undefined', function () {
                const item = new Djblets.ConfigFormsListItem({
                  text: 'Label'
                });
                item.setActions([{
                  enabledPropInverse: true,
                  enabledPropName: 'isDisabled',
                  id: 'mycheckbox',
                  label: 'Checkbox',
                  type: 'checkbox'
                }]);
                const itemView = new Djblets.ConfigFormsListItemView({
                  model: item
                });
                itemView.render();
                const $action = itemView.$('.config-forms-list-action-mycheckbox');
                window.expect($action.prop('disabled')).toBe(false);
              });
              window.it('value == true', function () {
                const item = new Djblets.ConfigFormsListItem({
                  isDisabled: true,
                  text: 'Label'
                });
                item.setActions([{
                  enabledPropInverse: true,
                  enabledPropName: 'isDisabled',
                  id: 'mycheckbox',
                  label: 'Checkbox',
                  type: 'checkbox'
                }]);
                const itemView = new Djblets.ConfigFormsListItemView({
                  model: item
                });
                itemView.render();
                const $action = itemView.$('.config-forms-list-action-mycheckbox');
                window.expect($action.prop('disabled')).toBe(true);
              });
              window.it('value == false', function () {
                const item = new Djblets.ConfigFormsListItem({
                  isDisabled: false,
                  text: 'Label'
                });
                item.setActions([{
                  enabledPropInverse: true,
                  enabledPropName: 'isDisabled',
                  id: 'mycheckbox',
                  label: 'Checkbox',
                  type: 'checkbox'
                }]);
                const itemView = new Djblets.ConfigFormsListItemView({
                  model: item
                });
                itemView.render();
                const $action = itemView.$('.config-forms-list-action-mycheckbox');
                window.expect($action.prop('disabled')).toBe(false);
              });
            });
          });
        });
      });
      window.describe('Action handlers', function () {
        window.it('Buttons', function () {
          const item = new Djblets.ConfigFormsListItem({
            text: 'Label'
          });
          item.setActions([{
            id: 'mybutton',
            label: 'Button'
          }]);
          const itemView = new Djblets.ConfigFormsListItemView({
            model: item
          });
          itemView.actionHandlers = {
            mybutton: '_onMyButtonClick'
          };
          itemView._onMyButtonClick = jasmine.createSpy('_onMyButtonClick');
          itemView.render();
          const $button = itemView.$('button.djblets-c-config-forms-list__item-action');
          window.expect($button.length).toBe(1);
          $button.click();
          window.expect(itemView._onMyButtonClick).toHaveBeenCalled();
        });
        window.it('Checkboxes', function () {
          const item = new Djblets.ConfigFormsListItem({
            checkboxAttr: false,
            text: 'Label'
          });
          item.setActions([{
            id: 'mycheckbox',
            label: 'Checkbox',
            propName: 'checkboxAttr',
            type: 'checkbox'
          }]);
          const itemView = new Djblets.ConfigFormsListItemView({
            model: item
          });
          itemView.actionHandlers = {
            mybutton: '_onMyButtonClick'
          };
          itemView._onMyButtonClick = jasmine.createSpy('_onMyButtonClick');
          itemView.render();
          const $checkbox = itemView.$('input[type=checkbox]');
          window.expect($checkbox.length).toBe(1);
          window.expect($checkbox.prop('checked')).toBe(false);
          $checkbox.prop('checked', true).triggerHandler('change');
          window.expect(item.get('checkboxAttr')).toBe(true);
        });
      });
    });

    window.suite('djblets/configForms/views/ListView', () => {
      let collection;
      let list;
      let listView;
      window.beforeEach(() => {
        collection = new Backbone.Collection([{
          text: 'Item 1'
        }, {
          text: 'Item 2'
        }, {
          text: 'Item 3'
        }], {
          model: Djblets.ConfigFormsListItem
        });
        list = new Djblets.ConfigFormsList({}, {
          collection: collection
        });
        listView = new Djblets.ConfigFormsListView({
          model: list
        });
      });
      window.describe('Methods', () => {
        window.describe('render', () => {
          window.it('On first render', () => {
            window.expect(listView.$listBody).toBeNull();
            window.expect(listView.$('li').length).toBe(0);
            listView.render();
            window.expect(listView.$listBody).toBe(listView.$el);
            window.expect(listView.$('li').length).toBe(3);
          });
          window.it('On subsequent render', () => {
            window.expect(listView.$listBody).toBeNull();
            window.expect(listView.$('li').length).toBe(0);

            /* First render. */
            listView.render();
            window.expect(listView.$listBody).toBe(listView.$el);
            window.expect(listView.$('li').length).toBe(3);

            /* Modify some state. */
            listView.$el.append('<button>');
            listView.$listBody = $('<input>');

            /* Second render. */
            listView.render();
            window.expect(listView.$listBody).toBe(listView.$el);
            window.expect(listView.$('li').length).toBe(3);
            window.expect(listView.$('button').length).toBe(0);
            window.expect(listView.$('input').length).toBe(0);
          });
        });
      });
      window.describe('Manages items', () => {
        window.beforeEach(() => {
          listView.render();
        });
        window.it('On render', () => {
          const $items = listView.$('li');
          window.expect($items.length).toBe(3);
          window.expect($items.eq(0).text().trim()).toBe('Item 1');
          window.expect($items.eq(1).text().trim()).toBe('Item 2');
          window.expect($items.eq(2).text().trim()).toBe('Item 3');
        });
        window.it('On add', () => {
          collection.add({
            text: 'Item 4'
          });
          const $items = listView.$('li');
          window.expect($items.length).toBe(4);
          window.expect($items.eq(3).text().trim()).toBe('Item 4');
        });
        window.it('On remove', () => {
          collection.remove(collection.at(0));
          const $items = listView.$('li');
          window.expect($items.length).toBe(2);
          window.expect($items.eq(0).text().trim()).toBe('Item 2');
        });
        window.it('On reset', () => {
          collection.reset([{
            text: 'Foo'
          }, {
            text: 'Bar'
          }]);
          const $items = listView.$('li');
          window.expect($items.length).toBe(2);
          window.expect($items.eq(0).text().trim()).toBe('Foo');
          window.expect($items.eq(1).text().trim()).toBe('Bar');
        });
      });
    });

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

    window.suite('djblets/configForms/views/TableItemView', function () {
      window.describe('Rendering', function () {
        window.describe('Item display', function () {
          window.it('With editURL', function () {
            const item = new Djblets.ConfigFormsListItem({
              editURL: 'http://example.com/',
              text: 'Label'
            });
            const itemView = new Djblets.ConfigFormsTableItemView({
              model: item
            });
            itemView.render();
            window.expect(itemView.$el.html().trim()).toBe(['<td>', '<span class="djblets-c-config-forms-list__item-actions">', '</span>\n\n', '<a href="http://example.com/">Label</a>\n\n', '</td>'].join(''));
          });
          window.it('Without editURL', function () {
            const item = new Djblets.ConfigFormsListItem({
              text: 'Label'
            });
            const itemView = new Djblets.ConfigFormsTableItemView({
              model: item
            });
            itemView.render();
            window.expect(itemView.$el.html().trim()).toBe(['<td>', '<span class="djblets-c-config-forms-list__item-actions">', '</span>\n\n', 'Label\n\n', '</td>'].join(''));
          });
        });
        window.describe('Action placement', function () {
          window.it('Default template', function () {
            const item = new Djblets.ConfigFormsListItem({
              text: 'Label'
            });
            item.setActions([{
              id: 'mybutton',
              label: 'Button'
            }]);
            const itemView = new Djblets.ConfigFormsTableItemView({
              model: item
            });
            itemView.render();
            const $button = itemView.$('td:last button.djblets-c-config-forms-list__item-action');
            window.expect($button.length).toBe(1);
            window.expect($button.text()).toBe('Button');
          });
          window.it('Custom template', function () {
            var _dec, _class, _class2;
            let CustomTableItemView = (_dec = Spina.spina({
              prototypeAttrs: ['template']
            }), _dec(_class = (_class2 = class CustomTableItemView extends Djblets.ConfigFormsTableItemView {}, _defineProperty(_class2, "template", _.template(`<td></td>
<td></td>`)), _class2)) || _class);
            const item = new Djblets.ConfigFormsListItem({
              text: 'Label'
            });
            item.setActions([{
              id: 'mybutton',
              label: 'Button'
            }]);
            const itemView = new CustomTableItemView({
              model: item
            });
            itemView.render();
            const $button = itemView.$('td:last button.djblets-c-config-forms-list__item-action');
            window.expect($button.length).toBe(1);
            window.expect($button.text()).toBe('Button');
          });
        });
      });
    });

    window.suite('djblets/configForms/views/TableView', () => {
      window.describe('Manages rows', () => {
        let collection;
        let list;
        let tableView;
        window.beforeEach(() => {
          collection = new Backbone.Collection([{
            text: 'Item 1'
          }, {
            text: 'Item 2'
          }, {
            text: 'Item 3'
          }], {
            model: Djblets.ConfigFormsListItem
          });
          list = new Djblets.ConfigFormsList({}, {
            collection: collection
          });
          tableView = new Djblets.ConfigFormsTableView({
            model: list
          });
          tableView.render();
        });
        window.it('On render', () => {
          const $rows = tableView.$('tr');
          window.expect($rows.length).toBe(3);
          window.expect($rows.eq(0).text().trim()).toBe('Item 1');
          window.expect($rows.eq(1).text().trim()).toBe('Item 2');
          window.expect($rows.eq(2).text().trim()).toBe('Item 3');
        });
        window.it('On add', () => {
          collection.add({
            text: 'Item 4'
          });
          const $rows = tableView.$('tr');
          window.expect($rows.length).toBe(4);
          window.expect($rows.eq(3).text().trim()).toBe('Item 4');
        });
        window.it('On remove', () => {
          collection.remove(collection.at(0));
          const $rows = tableView.$('tr');
          window.expect($rows.length).toBe(2);
          window.expect($rows.eq(0).text().trim()).toBe('Item 2');
        });
        window.it('On reset', () => {
          collection.reset([{
            text: 'Foo'
          }, {
            text: 'Bar'
          }]);
          const $rows = tableView.$('tr');
          window.expect($rows.length).toBe(2);
          window.expect($rows.eq(0).text().trim()).toBe('Foo');
          window.expect($rows.eq(1).text().trim()).toBe('Bar');
        });
      });
    });

}));
//# sourceMappingURL=index.js.map
