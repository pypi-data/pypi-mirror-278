## -*- coding: utf-8; -*-

<script type="text/javascript">

  ${form.component_studly}Data.quickbooksBankAccountShowDialog = false
  ${form.component_studly}Data.quickbooksBankAccountEditing = null
  ${form.component_studly}Data.quickbooksBankAccountStore = null
  ${form.component_studly}Data.quickbooksBankAccountNumber = null
  ${form.component_studly}Data.quickbooksBankAccountStoreOptions = ${json.dumps(store_options)|n}

  ${form.component_studly}.methods.quickbooksBankAccountCreate = function() {
      this.quickbooksBankAccountEditing = null
      this.quickbooksBankAccountStore = null
      this.quickbooksBankAccountNumber = null
      this.quickbooksBankAccountShowDialog = true
  }

  ${form.component_studly}.methods.quickbooksBankAccountEdit = function(row) {
      this.quickbooksBankAccountEditing = row
      this.quickbooksBankAccountStore = row.store_uuid
      this.quickbooksBankAccountNumber = row.account_number
      this.quickbooksBankAccountShowDialog = true
      this.$nextTick(() => {
          this.$refs.quickbooksBankAccountNumber.focus()
      })
  }

  ${form.component_studly}.computed.quickbooksBankAccountSaveDisabled = function(row) {
      if (!this.quickbooksBankAccountStore) {
          return true
      }
      if (!this.quickbooksBankAccountNumber) {
          return true
      }
      return false
  }

  ${form.component_studly}.computed.quickbooksBankAccountsFinal = function() {
      return JSON.stringify(this.quickbooksBankAccountsData)
  }

  ${form.component_studly}.methods.quickbooksBankAccountSave = function() {
      if (this.quickbooksBankAccountEditing) {
          this.quickbooksBankAccountEditing.store_uuid = this.quickbooksBankAccountStore
          this.quickbooksBankAccountEditing.account_number = this.quickbooksBankAccountNumber
          this.quickbooksBankAccountShowDialog = false
      } else {
          if (this.quickbooksBankAccountIsStoreDefined(this.quickbooksBankAccountStore)) {
              alert("An account number is already defined for that store!")
          } else {
              this.quickbooksBankAccountsData.push({
                  store_uuid: this.quickbooksBankAccountStore,
                  store: this.quickbooksBankAccountGetStoreDisplay(this.quickbooksBankAccountStore),
                  account_number: this.quickbooksBankAccountNumber,
              })
              this.quickbooksBankAccountShowDialog = false
          }
      }
  }

  ${form.component_studly}.methods.quickbooksBankAccountIsStoreDefined = function(uuid) {
      for (let account of this.quickbooksBankAccountsData) {
          if (account.store_uuid == uuid) {
              return true
          }
      }
      return false
  }

  ${form.component_studly}.methods.quickbooksBankAccountGetStoreDisplay = function(uuid) {
      for (let store of this.quickbooksBankAccountStoreOptions) {
          if (store.uuid == uuid) {
              return store.display
          }
      }
  }

  ${form.component_studly}.methods.quickbooksBankAccountDelete = function(row) {
      if (confirm("Really delete this account number?")) {
          let i = this.quickbooksBankAccountsData.indexOf(row)
          this.quickbooksBankAccountsData.splice(i, 1)
          this.quickbooksBankAccountShowDialog = false
      }
  }

</script>
