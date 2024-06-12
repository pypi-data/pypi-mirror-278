!function(){var t,e;t=function(){},"function"==typeof define&&define.amd&&define(t),Djblets.AddIntegrationPopupView=Backbone.View.extend({className:"djblets-c-integrations-popup",integrationTemplateSource:`<li class="djblets-c-integration">
 <a href="<%- addURL %>">
  <% if (iconSrc) { %>
   <img class="djblets-c-integration__icon"
        src="<%- iconSrc %>"
        srcset="<%- iconSrcSet %>"
        width="48" height="48" alt="">
  <% } %>
  <div class="djblets-c-integration__details">
   <div class="djblets-c-integration__name"><%- name %></div>
   <div class="djblets-c-integration__description">
    <%- description %>
   </div>
  </div>
 </a>
</li>`,emptyIntegrationsTemplateSource:`<p class="djblets-c-integrations-popup__empty">
 ${_.escape(gettext("There are no integrations currently installed."))}
</p>`,initialize(t){this.integrations=t.integrations},render(){var e=this.integrations;if(0<e.length){var i=_.template(this.integrationTemplateSource),n=$("<ul>");for(let t=0;t<e.length;t++)n.append(i(e[t]));this.$el.append(n)}else this.$el.addClass("-is-empty").append(_.template(this.emptyIntegrationsTemplateSource)());return this},remove(){this.hide(),Backbone.View.prototype.remove.call(this)},show(e){var i=$(window),n=this.$el,s=this.el,o=e.position(),o=(n.move(o.left,o.top+e.outerHeight(),"absolute").width(100).height(1).show(),n.getExtents("b","lr")),e=s.offsetWidth-s.clientWidth-o,l=n.offset(),a=Math.floor(i.height()-l.top-n.getExtents("bm","tb"));if(n.css({height:"auto","max-height":a}),n.hasClass("-is-empty"))n.css("width","auto");else{var a=n.find(".djblets-c-integration").filter(":first").outerWidth(!0),i=i.width(),r=i-l.left-e-n.getExtents("m","r");let t=Math.max(Math.floor(r/a),1)*a+e+o;n.outerWidth(t),0==s.offsetWidth-s.clientWidth-o&&(t-=e,n.outerWidth(t)),l.left+t>i&&n.css("left",i-t)}$(document).one("click.djblets-integrations-popup",()=>this.hide()),$(window).one("resize.djblets-integrations-popup",()=>this.hide())},hide(){this.$el.hide(),$(document).off("click.djblets-integrations-popup"),$(window).off("resize.djblets-integrations-popup")}}),t=Djblets.Config.ListItem.extend({defaults:_.defaults({removeLabel:gettext("Delete"),showRemove:!0},Djblets.Config.ListItem.prototype.defaults),url(){return this.get("editURL")},parse(t){return{editURL:t.editURL,id:t.id,integrationID:t.integrationID,itemState:t.enabled?"enabled":"disabled",name:t.name}}}),e=Djblets.Config.TableItemView.extend({className:"djblets-c-integration-config djblets-c-config-forms-list__item",actionHandlers:{delete:"_onDeleteClicked"},template:_.template(`<td class="djblets-c-integration-config__name">
 <img src="<%- iconSrc %>"
      srcset="<%- iconSrcSet %>"
      width="32" height="32" alt="">
 <a href="<%- editURL %>"><%- name %></a>
</td>
<td class="djblets-c-integration-config__integration-name">
 <%- integrationName %>
</td>
<td class="djblets-c-config-forms-list__item-state"></td>
<td></td>`),getRenderContext(){var t=this.model.get("integrationID"),t=this.model.collection.options.integrationsMap[t];return{iconSrc:t.iconSrc,iconSrcSet:t.iconSrcSet,integrationName:t.name}},_onDeleteClicked(){$("<p>").text(gettext("This integration will be permanently removed. This cannot be undone.")).modalBox({buttons:[$("<button>").text(gettext("Cancel")),$('<button class="danger">').text(gettext("Delete Integration")).click(()=>this.model.destroy({beforeSend:t=>{t.setRequestHeader("X-CSRFToken",this.model.collection.options.csrfToken)}}))],title:gettext("Are you sure you want to delete this integration?")})}}),Djblets.IntegrationConfigListView=Backbone.View.extend({events:{"click .djblets-c-integration-configs__add":"_onAddIntegrationClicked"},addIntegrationPopupViewType:Djblets.AddIntegrationPopupView,listItemType:t,listItemViewType:e,listItemsCollectionType:Djblets.Config.ListItems,listViewType:Djblets.Config.TableView,initialize(t){this._integrationIDs=t.integrationIDs,this._integrationsMap=t.integrationsMap,this.list=new Djblets.Config.List({},{collection:new this.listItemsCollectionType(t.configs,{csrfToken:t.csrfToken,integrationsMap:t.integrationsMap,model:this.listItemType,parse:!0})}),this._popup=null},render(){return this.listView=new this.listViewType({ItemView:this.listItemViewType,el:this.$(".djblets-c-config-forms-list"),model:this.list}),this.listView.render().$el.removeAttr("aria-busy"),this._$listContainer=this.listView.$el.parent(),this.listenTo(this.list.collection,"add remove",this._showOrHideConfigsList),this._showOrHideConfigsList(),this},_showOrHideConfigsList(){0<this.list.collection.length?this._$listContainer.show():this._$listContainer.hide()},_onAddIntegrationClicked(t){if(t.preventDefault(),t.stopPropagation(),!this._popup){var e=this._integrationIDs,i=this._integrationsMap,n=[];for(let t=0;t<e.length;t++)n.push(i[e[t]]);this._popup=new this.addIntegrationPopupViewType({integrations:n}),this._popup.render().$el.appendTo(this.$el)}this._popup.show($(t.target))}})}.call(this);
