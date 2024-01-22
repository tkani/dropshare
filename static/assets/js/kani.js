
// ------------------------------------------------- Security Change --------------------------------------------------
  function security_change(value,file_type) {
    // Show the modal when the icon is clicked
      $("#securityModal_" + value).modal('show');
  }
  function security_submitPassword(value,file_type) {
        // Get the entered email
    // alert(value)
        var security = $("#securityInput_" + value).val();

        // Get the item ID from the modal data attribute
        var itemId = value;

        var url_link = '/api/data_house/';
        var keyword = 'security';
        var data = {'file_id': itemId,
                    'file_type':file_type,
                    'password':security};

        // Perform password validation
        validatesecurityfile(itemId, data, url_link, keyword, function (isValidPassword, errorMessage) {
            if (!isValidPassword) {
                $("#securityInput_" + value).val("");
                alert(errorMessage);
            } else {
                // Clear the email input
                $("#securityInput_" + value).val("");
                $("#securityModal_" + value).modal('hide');
            }
        });
    };
     // Function to validate the password
    function validatesecurityfile(itemId, data, url_link, keyword, callback,) {
        var apiEndpoint = url_link;
        var accessToken = "{{session}}";

        $.ajax({
            url: apiEndpoint,
            type: 'PUT',
            headers: {
                'X-access-token': accessToken
            },
            data: {
                'file_id': itemId,
                'data' : JSON.stringify(data),
            },
            success: function (response) {
              
              if (keyword == 'security')
              {
                console.log(data)

                if ('message' in response) {
                  if (response.new_file_type == 'Protected'){
                      var click_method = 'security_change'
                      var iframe='ri-admin-fill'


                      document.getElementById('file_name_'+response.file_id).innerHTML=`
                      <div class="icon icon-grid i-grid ltc">
                          <div class="icon-small bg-primary rounded mr-3">
                              <i class="ri-file-download-line"></i>
                          </div>
                          <a style="color:#8f93f6; cursor:pointer;" id="${response.file_id}" title="${response.file_original_name}" onclick="download_link(${response.file_id})">${response.file_original_name}</a>
                      </div>`;

                      document.getElementById('download_file_'+response.file_id).innerHTML=`<a style="color:#535f6b;; cursor:pointer;" id="${response.file_id}" ><i class="ri-file-lock-fill" onclick="download_link(${response.file_id})"> Download</a></i>`;
                  }
                  else if (response.new_file_type == 'Public'){
                    var click_method = 'security_submitPassword'
                      var iframe='ri-team-fill'

                      document.getElementById('file_name_'+response.file_id).innerHTML=`
                      <div class="icon icon-grid i-grid ltc">
                          <div class="icon-small bg-primary rounded mr-3">
                              <i class="ri-file-download-line"></i>
                          </div>
                          <a href="/api_download_files/?image_token=${response.access_token}"  title="${response.file_original_name}">${response.file_original_name}</a>

                          </td>
                      </div>`;
                      
                    document.getElementById('download_file_'+response.file_id).innerHTML=`<a <a href="/api_download_files/?image_token=${response.access_token}" ><i class="ri-download-cloud-fill" style="color:#535f6b;">Download</a></i>`;
                  }
                    else
                    {
                      var click_method = 'security_change'
                      var iframe='ri-user-fill'
                    }
                    console.log(response)
                    new_modal=`<i class="${iframe}" style="cursor:pointer;" onclick="${click_method}(${response.file_id},'${response.new_file_type}')" >${response.new_file_type}</i>`

                    document.getElementById('file_type_'+response.file_id).innerHTML=new_modal;
                    document.getElementById('file_sub_type_'+response.file_id).innerHTML=`<button type="button" class="btn btn-primary" onclick="security_submitPassword(${response.file_id},'${response.new_file_type}')">Submit</button>`;
                    callback(true,response);
                } else {
                  console.log(response)
                    console.log('Error: Invalid To File Id');
                    callback(false, 'Invalid File');
                }
              }
              
            },
            error: function (jqXHR,error) {
                console.log('Error:', jqXHR.responseJSON);
                callback(false,jqXHR.responseJSON.error || 'Contact Admin Support.');
            }
        });
    }
  // ---------------------------------------------- Share Property -----------------------------------------------------
   function shareModal(value) {
        // Show the modal when the icon is clicked
        $("#shareModals_" + value).modal('show');
    }

   function submit_shareduser(value) {
        // Get the entered email
        var email_id = $("#emailInput_" + value).val();
        var password = $("#passwordInput_" + value).val();

        // Get the item ID from the modal data attribute
        var itemId = value;

        var url_link = '/api/get_shared_file/';
        var keyword = 'share';
        var data = {'email_id': email_id,
                    'password':password};

        // Perform password validation
        validatePassword(itemId, data, url_link, keyword, function (isValidPassword, errorMessage) {
            if (!isValidPassword) {
                alert(errorMessage);
            } else {
                // Clear the email input
                $("#emailInput_" + value).val("");
                $("#passwordInput_" + value).val("");
                // Optionally, you can close the modal after handling the input
                // $("#shareModals_" + value).modal('hide');
            }
        });
    };

    // ---------------------------------------------- Property delete-----------------------------------------------------
    function delete_property(value) {
      // Show the modal when the icon is clicked
      $("#delete_passwordModal_" + value).modal('show');
  }
    function file_submitPassword(value) {
        // Get the item ID from the modal data attribute
        var itemId = value;
        var password = document.getElementById('delete_passwordInput_'+value).value;
        var url_link = '/api/delete_file/';
        var keyword = 'delete_file';
        var data = {'password': password};

        // Perform password validation
        validate_delete_file_fun(itemId, data, url_link, keyword, function (isValidPassword, response) {
            if (!isValidPassword) {
                alert(response);
            } else {
                alert('File Deleted!!');
                 $("#delete_passwordModal_" + value).modal('hide');
            }
        });
    };
    // Function to validate the password
    function validate_delete_file_fun(itemId, data, url_link, keyword, callback,) {
        var apiEndpoint = url_link;
        var accessToken = "{{session}}";

        $.ajax({
            url: apiEndpoint,
            type: 'DELETE',
            headers: {
                'X-access-token': accessToken
            },
            data: {
                'file_id': itemId,
                'data' : JSON.stringify(data),
            },
            success: function (response) {
              
              if (keyword == 'delete_file')
              {

                if ('message' in response) {
                    $('#file_' +response.file_id).remove();
                    
                    callback(true,response);
                } else {
                  console.log(response)
                    console.log('Error: Invalid To File Id');
                    callback(false, 'Invalid File');
                }
              }
              
            },
            error: function (jqXHR,error) {
                console.log('Error:', jqXHR.responseJSON);
                callback(false,jqXHR.responseJSON.error || 'Contact Admin Support.');
            }
        });
    }
    // ---------------------------------------------- Share Property delete-----------------------------------------------------
    function delete_shared(value,to_user_id) {
        // Get the entered email
        var to_user_id = to_user_id

        // Get the item ID from the modal data attribute
        var itemId = value;

        var url_link = '/api/get_shared_file/';
        var keyword = 'delete_share';
        var data = {'to_user_id': to_user_id};

        // Perform password validation
        validate_delete_fun(itemId, data, url_link, keyword, function (isValidPassword, errorMessage) {
            if (!isValidPassword) {
                alert(errorMessage);
            } else {
                alert('User Removed!!');
            }
        });
    };
    // Function to validate the password
    function validate_delete_fun(itemId, data, url_link, keyword, callback,) {
        var apiEndpoint = url_link;
        var accessToken = "{{session}}";

        $.ajax({
            url: apiEndpoint,
            type: 'DELETE',
            headers: {
                'X-access-token': accessToken
            },
            data: {
                'file_id': itemId,
                'data': JSON.stringify(data)
            },
            success: function (response) {
              
              if (keyword == 'delete_share')
              {

                if ('message' in response) {
                    $('#card_user_'+response.to_user_id).empty();;
                    
                    callback(true,response);
                } else {
                  console.log(response)
                    console.log('Error: Invalid To user Id');
                    callback(false, 'Invalid Email Id');
                }
              }
              
            },
            error: function (jqXHR,error) {
                console.log('Error:', jqXHR.responseJSON);
                callback(false,jqXHR.responseJSON.error || 'Contact Admin Support.');
            }
        });
    }
    // --------------------------------------------------- Password Property -----------------------------------------------
    function download_link(value) {
      // Show the modal when the icon is clicked
      $("#passwordModal_" + value).modal('show');
  }

    function submitPassword(value) {
        var itemId=value;
        // Get the entered password
        var password = document.getElementById('passwordInput_'+itemId).value;

        // Get the item ID from the modal data attribute
        var itemId = value;
        var url_link='/api/get_secured_file/'
        var keyword='download'
        var data= {'password':password}
        // Perform password validation
        validatePassword(itemId, data,url_link,keyword, function (isValidPassword, errorMessage) {
            if (!isValidPassword) {
                document.getElementById('passwordInput_'+itemId).value=""
                alert(errorMessage);
            }
            else
            {
              document.getElementById('passwordInput_'+itemId).value=""
              $('#passwordModal_'+itemId).modal('hide');
            }
        });
    };

    
    // Function to validate the password
    function validatePassword(itemId, data, url_link, keyword, callback,) {
        var apiEndpoint = url_link;
        var accessToken = "{{session}}";

        $.ajax({
            url: apiEndpoint,
            type: 'POST',
            headers: {
                'X-access-token': accessToken
            },
            data: {
                'file_id': itemId,
                'data': JSON.stringify(data)
            },
            success: function (response) {

              if (keyword == 'download')
              {

                if ('file_name' in response && 'save_name' in response) {
                    // Construct the download URL using the received file details
                    var downloadUrl = `/api_download_files/?image_token=${response.access_token}`

                    // Trigger the file download
                    window.location.href = downloadUrl;
                    callback(true);
                } else {
                  console.log(response)
                    console.log('Error: Invalid file password');
                    callback(false, 'Invalid file password');
                }
              }
              else if (keyword == 'share')
              {
                console.log(response)
                if ('profile_image' in response && 'name' in response && 'email_id' in response && 'to_user_id' in response) {
                    // Construct the download URL using the received file details
                    var newModelContent = `<div class="card-body" id="card_user_${response.to_user_id}" >
                                                <div class="profile-header">
                                                  <div class="cover-container text-center">
                                                      <div class="cover-container">
                                                          <div class="row align-items-center">
                                                            <div class="col-lg-3">
                                                                <!-- Image on the left -->
                                                                <img class="rounded-circle profile-icon bg-primary d-block" src="/media/${response.profile_image}">
                                                            </div>
                                                            <div class="col-lg-6 text-center">
                                                                <!-- Name in the center -->
                                                                <p class="mt-2" style="margin-bottom: 0px;">${response.name}</p>
                                                                <p style="display: inline-block;">${response.email_id}</p>
                                                            </div>
                                                            <div class="col-lg-3">
                                                              <span class="mt-3 float-right">
                                                                      <!-- j.to_user_id__email_id -->
                                                                        <i class="ri-delete-bin-fill" style="cursor:pointer;" onclick="delete_shared(${itemId},'${response.to_user_id}')"></i>
                                                                    </span>
                                                            </div>
                                                          </div>
                                                      </div>
                                                  </div>
                                                </div>
                                              </div>`
                    $("#shared_users_"+itemId).append(newModelContent);
                    // Trigger the file download
                    callback(true);
                } else {
                    console.log('Error: Invalid response format');
                    callback(false,jqXHR.responseJSON.error || 'Contact Admin Support.');
                }
              }
            },
            error: function (jqXHR,error) {
                console.log('Error:', jqXHR.responseJSON);
                callback(false,jqXHR.responseJSON.error || 'Contact Admin Support.');
            }
        });
    }
    // --------------------------------------------------------------------------------------------------------------------

