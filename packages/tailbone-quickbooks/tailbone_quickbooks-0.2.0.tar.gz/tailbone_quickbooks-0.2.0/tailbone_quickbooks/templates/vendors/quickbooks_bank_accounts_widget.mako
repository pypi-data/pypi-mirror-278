## -*- coding: utf-8; -*-

<div style="display: flex;">
  <span style="flex-grow: 1;"></span>
  <b-button type="is-primary"
            icon-pack="fas"
            icon-left="plus"
            @click="quickbooksBankAccountCreate()">
    Add Account
  </b-button>
</div>

${grid.render_table_element(data_prop='quickbooksBankAccountsData')|n}

<b-modal has-modal-card
         :active.sync="quickbooksBankAccountShowDialog">
  <div class="modal-card">

    <header class="modal-card-head">
      <p class="modal-card-title">Quickbooks Bank Account</p>
    </header>

    <section class="modal-card-body">

      <b-field label="Store"
               :type="{'is-danger': !quickbooksBankAccountStore}">
        <b-select v-model="quickbooksBankAccountStore"
                  :disabled="quickbooksBankAccountEditing">
          <option v-for="store in quickbooksBankAccountStoreOptions"
                  :key="store.uuid"
                  :value="store.uuid">
            {{ store.display }}
          </option>
        </b-select>
      </b-field>

      <b-field label="Account Number"
               :type="{'is-danger': !quickbooksBankAccountNumber}">
        <b-input v-model="quickbooksBankAccountNumber"
                 ref="quickbooksBankAccountNumber" />
      </b-field>

    </section>

    <footer class="modal-card-foot">
      <b-button type="is-primary"
                @click="quickbooksBankAccountSave()"
                :disabled="quickbooksBankAccountSaveDisabled"
                icon-pack="fas"
                icon-left="save">
        Update
      </b-button>
      <b-button @click="quickbooksBankAccountShowDialog = false">
        Cancel
      </b-button>
    </footer>
  </div>
</b-modal>
