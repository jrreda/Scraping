import helper

# Register
helper.register()

# logout
helper.logout(is_after_becomeAsupplier=False)

# SIGN back IN
helper.sign_in()

# BECOME A SUPPLIER from buyer
helper.become_a_supplier(helper.is_required, is_from_buyer=True)

# CONTACT US
helper.contact_us(is_logged=True)

# Search for fire alarm
helper.search()

# specific RFQ
helper.submit_rfq(helper.is_required)

# LOGOUT
helper.logout(is_after_becomeAsupplier=True)

# Become A Supplier
helper.become_a_supplier(helper.is_required, is_from_buyer=False)