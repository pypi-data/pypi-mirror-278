export const id=548;export const ids=[548];export const modules={8548:(e,i,o)=>{o.r(i),o.d(i,{ProgressDialog:()=>n});var t=o(5461),a=(o(3279),o(924)),s=o(993),r=o(3799),d=o(3167);let n=(0,t.A)([(0,s.EM)("progress-dialog")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,s.P)("ha-dialog",!0)],key:"_dialog",value:void 0},{kind:"method",key:"showDialog",value:async function(e){this._params=e,await this.updateComplete,(0,d.r)(this._dialog,"iron-resize")}},{kind:"method",key:"closeDialog",value:async function(){this.close()}},{kind:"method",key:"render",value:function(){var e,i;return this._params?a.qy`
      <ha-dialog open scrimClickAction escapeKeyAction @close-dialog=${this.closeDialog}>
        <h2>${null===(e=this._params)||void 0===e?void 0:e.title}</h2>
        <p>${null===(i=this._params)||void 0===i?void 0:i.text}</p>

        <div id="dialog-content">
          <ha-circular-progress active></ha-circular-progress>
        </div>
      </ha-dialog>
    `:a.s6}},{kind:"method",key:"close",value:function(){this._params=void 0}},{kind:"get",static:!0,key:"styles",value:function(){return[r.nA,a.AH`
        #dialog-content {
          text-align: center;
        }
      `]}}]}}),a.WF)}};
//# sourceMappingURL=JrHvBPiV.js.map