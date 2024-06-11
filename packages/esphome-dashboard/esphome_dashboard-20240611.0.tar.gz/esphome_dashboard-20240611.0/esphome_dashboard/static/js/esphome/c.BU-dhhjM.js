import{I as o,b as t,d as i,l as s,n as e,s as a,x as n,K as l,j as d}from"./index-sRtbOpnj.js";import"./c.BjZ0sBSR.js";import"./c.C9lgy-8S.js";let c=class extends a{render(){const o=void 0===this._valid?"":this._valid?"✅":"❌";return n`
      <esphome-process-dialog
        .heading=${`Validate ${this.configuration} ${o}`}
        .type=${"validate"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){l(this.configuration)}_openInstall(){d(this.configuration)}_handleProcessDone(o){this._valid=0==o.detail}_handleClose(){this.parentNode.removeChild(this)}};c.styles=[o],t([i()],c.prototype,"configuration",void 0),t([s()],c.prototype,"_valid",void 0),c=t([e("esphome-validate-dialog")],c);
//# sourceMappingURL=c.BU-dhhjM.js.map
