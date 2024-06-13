import{I as o,b as t,d as s,n as i,s as e,x as n,K as a,j as l}from"./index-B_W6eoJm.js";import"./c.CuMEVZD2.js";import"./c.hWjR1jlG.js";let c=class extends e{render(){return n`
      <esphome-process-dialog
        .heading=${`Clean ${this.configuration}`}
        .type=${"clean"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
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
    `}_openEdit(){a(this.configuration)}_openInstall(){l(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};c.styles=[o],t([s()],c.prototype,"configuration",void 0),c=t([i("esphome-clean-dialog")],c);
//# sourceMappingURL=c.DPoJ5RMP.js.map
