import{I as e,r as t,b as o,d as a,n as i,s as n,x as l,H as s,h as d}from"./index-B_W6eoJm.js";import"./c.hWjR1jlG.js";let r=class extends n{render(){return l`
      <mwc-dialog
        .heading=${`Delete ${this.name}`}
        @closed=${this._handleClose}
        open
      >
        <div>Are you sure you want to delete ${this.name}?</div>
        <mwc-button
          slot="primaryAction"
          class="warning"
          label="Delete"
          dialogAction="close"
          @click=${this._handleDelete}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          no-attention
          label="Cancel"
          dialogAction="cancel"
        ></mwc-button>
      </mwc-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}async _handleDelete(){await s(this.configuration),d(this,"deleted")}};r.styles=[e,t`
      .warning {
        --mdc-theme-primary: var(--alert-error-color);
      }
    `],o([a()],r.prototype,"name",void 0),o([a()],r.prototype,"configuration",void 0),r=o([i("esphome-delete-device-dialog")],r);
//# sourceMappingURL=c.DFFPpW4x.js.map
