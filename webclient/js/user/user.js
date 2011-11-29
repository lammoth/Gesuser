jQuery.fn.reset = function () {
  $(this).each (function() {this.reset();});
}

/**
 *	Este archivo engloba las operaciones más comunes e independientes de las clases específicas:
 *		1- Clase Fechas: operaciones de fechas y horas
 *		2- Clase GUI: operaciones a nivel de interfaz
 *		3- Manejadores de los eventos más comunes, como son los "click" y los "submit" de los formularios
 */

var USER_GUI = {
    left_menu: '#left_section',
	users_table: '#user_search_list',
    edit_user_frm: '#user_edit_form',
    last_data_search: null,
    batch_user_file: null,
    response_batch_users: [],
    iq_list_id: [],
    no_users_add_batch: 0,
    no_users_error_batch: 0,
    total_entries_batch_users: 0,
    no_delete_users: 0,
    options_bubble: {
            selectable: false,
            position : 'bottom',
            align	 : 'center',
            innerHtml: _translate('Module inactive'),
            innerHtmlStyle: {
                                color:'#FFFFFF',
                                'text-align':'center'
                            },
            tail: {
                    align:'center',
                    hidden: false
                  },
            themeName: 	'all-black',
            themePath: 	'img/jquerybubblepopup-theme'
    },
    create_user_bubble_info: function(obj){
        $(obj).CreateBubblePopup({
                selectable: false,
                position : 'right',
                align	 : 'center',
                innerHtml: $(obj).attr('title'),
                innerHtmlStyle: {
                                    color:'#FFFFFF',
                                    'text-align':'center'
                                },
                tail: {
                        align:'center',
                        hidden: false
                      },
                themeName: 	'all-azure',
                themePath: 	'img/jquerybubblepopup-theme'
        });
        console.log('polla boba del user');
    }
}

var UserOperations = {
	/**
	 *	Recibe un conjunto de datos obtenidos a partir del item de un iq, el conjunto de datos es de la siguiente forma:
	 *	{uid: uid, gecos: gecos, quota: quota, course: course, group: group, profile: profile, pair: pair}
	 */
	print_user_result: function(data){
        USER_GUI.last_data_search = data;
        if (!data.error) {
            $('#remove_selected_items').fadeIn('slow');
            $.each(jQuery(':input[type=checkbox]:input[name=check_all]', $('#user_search_list')), function(){
                $(this).attr('disabled', false);
            });
        } else {
            $('#remove_selected_items').fadeOut('fast');
            $.each(jQuery(':input[type=checkbox]:input[name=check_all]', $('#user_search_list')), function(){
                $(this).attr('disabled', true);
            });
        }
		$.post('php/user/_get_user.php', data, function(data){
            XMPPDebug.log(data);
            var jsonData = $.parseJSON(data);
            if(jsonData.error){
                GUI.msg('error', jsonData.error);
                //XMPPDebug.log('error');
            } else {
                XMPPDebug.log(jsonData.user_html);
                $(USER_GUI.users_table+' tbody').fadeOut('fast', function () {
                    $(USER_GUI.users_table+' tbody').remove();
                    $(USER_GUI.users_table+' tbody').fadeIn('fast');
                    $(USER_GUI.users_table).append(jsonData.user_html);
                });
                //$(jsonData.user_html).appendTo('#users');
            }
        });
	},
    /**
	 *	Creación de usuario.
	 *	Manda los campos del formulario al objeto xmpp para que cree la stanza de creación de usuario
	 */
	create_user: function(){
        if (!USER_GUI.batch_user_file) {
            //console.log(pruebas);
            if(!Common.validate_form($(GUI.main_frm))){
                var fields = $(GUI.main_frm).serializeArray();
                var pass__position;

                //el campo pass ha de ir codificado en sha1
                $.each(fields, function (i, field){
                    if(field.name == 'pwd'){
                        field.value = '{SHA}'+hex_sha1(field.value);
                    }
                    else if(field.name == 'pwd2'){
                        field.value = hex_sha1(field.value);
                        pass__position = i;
                    }
                });

                //eliminamos el elemento "pass_"
                if(pass__position){
                    fields.splice(pass__position,1);
                }

                console.log(fields);
                XMPP.send_iq(fields, {etq:'user', type:'set', action:'create'});
                Common.session_renove();
            }
		} else {
            console.log("fucker entra en batch_users");
            UserOperations.create_batch_users();
        }
	},
    create_batch_users: function (){
        //XMPPDebug.log(USER_GUI.response_batch_users);
        //var prueba = new Array();
        USER_GUI.iq_list_id = [];
        USER_GUI.total_entries_batch_users = USER_GUI.response_batch_users.length;
        USER_GUI.no_users_add_batch = 0;
        USER_GUI.no_users_error_batch = 0;
        $('#user_batch_log').slideDown("fast");
        console.log(USER_GUI.response_batch_users);
        $('#user_batch_no_add').html('0/'+USER_GUI.total_entries_batch_users);
        $('#user_batch_no_del').html('0');
        $.each(USER_GUI.response_batch_users, function() {
            if (this.length > 5) {
                //console.log(this[0]);
                //XMPPDebug.log(this);
                // Create the users
                if (this[2] == "a") {
                    this[2] = "1";
                } else if (this[2] == "g") {
                    this[2] = "2";
                } else if (this[2] == "p") {
                    this[2] = "3";
                }
                var batch_user = new Array(/*{name:"item", value:new Array(*/
                                                                {name:"uid",value:this[0]},
                                                                {name:"pwd",value:'{SHA}' + hex_sha1(this[0])},
                                                                {name:"gecos",value:this[1]},
                                                                {name:"group",value:this[2]},
                                                                {name:"profile",value:this[3]},
                                                                {name:"course",value:this[4]},
                                                                {name:"quota",value:this[5]}
                                                            /*)
                                           }*/
                                       );
                //prueba.push(batch_user);
                /*$.each(batch_user, function(i, field) {
                    console.log(field.name + ":" + field.value);
                });*/
                //XMPPDebug.log(batch_user);
                console.log(batch_user);
                var id = XMPP.send_iq(batch_user, {etq:'user', type:'set', action:'create'});
                USER_GUI.iq_list_id.push({id:id,type:'user:create',result:'', iq:{uid:this[0]}});
                //console.log(identificador);
                //setTimeout(function(){}, 4000);
            }
        });
        //var a = new Array({name:"item",value:prueba});
        //XMPP.send_batch_iq(a, {etq:'user', type:'set', action:'create'});
        //USER_GUI.batch_user_file = null
        UserOperations.restablish_user_fileupload();
    },
    update_log_system: function(id) {
        var total_batch_add_users = 0;
        var total_batch_error_users = 0;
        $.each(USER_GUI.iq_list_id, function() {
            if (this.type == 'user:create') {
                if (this.result == 'result') {
                    total_batch_add_users += 1;
                } else if (this.result == 'error'){
                    total_batch_error_users += 1;
                }
            }
        });

        if (total_batch_add_users > 0) {
            if (total_batch_add_users >= USER_GUI.no_users_add_batch) {
                USER_GUI.no_users_add_batch = total_batch_add_users;
                 $('#user_batch_no_add').html(USER_GUI.no_users_add_batch+'/'+USER_GUI.total_entries_batch_users);
                 $.each(USER_GUI.iq_list_id, function() {
                     if (this.type == 'user:create' && this.result == 'result' && this.id == id){
                        $('#user_batch_new_names').append('<a><span>'+this.iq.uid+' </span></a>');
                     }
                 });
            }
        } else {
            $('#user_batch_no_add').html('0/'+USER_GUI.total_entries_batch_users);

        }

        if (total_batch_error_users > 0) {
            if (total_batch_error_users >= USER_GUI.no_users_error_batch) {
                USER_GUI.no_users_error_batch = total_batch_error_users;
                $('#user_batch_no_error').html(USER_GUI.no_users_error_batch);
                $.each(USER_GUI.iq_list_id, function() {
                     if (this.type == 'user:create' && this.result == 'error' && this.id == id){
                        $('#user_batch_error_names').append('<a><span>'+this.iq.uid+' </span></a>');
                     }
                });
            }
        } else {
            $('#user_batch_no_error').html('0');

        }
    },
    restablish_user_fileupload: function(){
        $("#user_delete_file").hide();
        USER_GUI.batch_user_file = null;
        USER_GUI.response_batch_users = [];
        $('#file_uploader').attr('disabled', false);
        $('#file_uploader').parent().show();
        $('#file_uploader').parent().parent().find('li').each(function(){
            $(this).remove();
        });
        $('#user_batch_new_names').find('a').each(function(){
            $(this).remove();
        });
        $('#user_batch_error_names').find('a').each(function(){
            $(this).remove();
        });
    },

    edit_user: function(){
		if(!Common.validate_form($(USER_GUI.edit_user_frm))){
			var fields = $(USER_GUI.edit_user_frm).serializeArray();
			var pass__position;

			//el campo pass ha de ir codificado en sha1
			$.each(fields, function (i, field){
				if(field.name == 'pwd' && field.value){
					field.value = '{SHA}'+hex_sha1(field.value);
				}
				else if(field.name == 'pwd2' && field.value){
					field.value = hex_sha1(field.value);
					pass__position = i;
				}
			});

			//eliminamos el elemento "pass_"
			if(pass__position){
				fields.splice(pass__position,1);
			}

			XMPP.send_iq(fields, {etq:'user', type:'set', action:'update'});
			Common.session_renove();
            return true;
		} else {
            return false;
        }
	},
	/**
	 *	Este caso es una mierda muy particular: para crear el array que se le pasa a la función XMPP.send_iq de manera
	 *	dinámica hay que sobrecargar mucho el html.
	 *
	 *	El array "fields" debe estar compuesto de objectos con los siguientes atributos:
	 *		- name
	 *		- value
	 *		- op
	 *
	 *	Para crearlo recorremos los <tr class="searching"> y buscamos dentro de ellos los elementos con class name, value y op, respectivamente.
	 */
	search_users: function(){
		$("#check_all").attr('checked', false);
        var fields = [];

		$.each(jQuery('tr.searching', GUI.main_frm), function(){
			var object = new Object();

			object.name = $(this).find('.name').val();
			object.value = $(this).find('.value').val();
			object.op = $(this).find('.op').val();

			if (object.value) {
				fields.push(object);
            } else {
                XMPPDebug.log(object.name);
                if (!object.value && (object.name == 'gecos' || object.name == 'uid')) {
                    object.value = '*';
                    fields.push(object);
                }
            }
		});

        Common.stanza_sended = fields;
		XMPP.send_iq(fields, {etq:'user', type:'get', action:'read'});
		Common.session_renove();
	},

    search_last_users: function(){
		var fields = Common.stanza_sended;
		XMPP.send_iq(fields, {etq:'user', type:'get', action:'read'});
		Common.session_renove();
	},

    check_all_items: function(){
        if ($('#check_all').attr('checked')) {
            $.each(jQuery(':input[type=checkbox]:input[name=element_sel]',$('#user_search_list')), function(){
                $(this).attr('checked', true);
            });
        } else {
            $.each(jQuery(':input[type=checkbox]:input[name=element_sel]',$('#user_search_list')), function(){
                $(this).attr('checked', false);
            });
        }
     },

	/**
	 *	Eliminación de un usuario (una vez confirmado)
	 *	Crea el array de campos que recibe la función encargada del envío de la <iq> con el formato deseado
	 */
	delete_user: function(uid){
		var fields = [];
		var field = new Object();
		field.name = 'uid';
		field.value = uid;
		fields.push(field);

        $('#remove_selected_items img').show();
        USER_GUI.no_delete_users += 1;
        console.log(USER_GUI.no_delete_users);

		XMPP.send_iq(fields, {etq:'user', type:'set', action:'delete'});
		Common.session_renove();
	},

    remove_check_items: function(){
        var user = _translate("users selected");
        $.get('php/user/_del_user.php',{user: user}, function(data){
			$('#del_dialog').html(data).dialog({height: 120,
                                                title: _translate("Delete user"),
                                                resizable: false,
                                                modal: true,
                                                buttons: {
                                                    "Cancelar": function() {$(this).dialog("close");},
                                                    "Eliminar": function() {
                                                        $.each(jQuery(':input[type=checkbox]:input[name=element_sel]',$('#user_search_list')), function(){
                                                            if ($(this).attr('checked')) {
                                                                var user_uid = new Array();
                                                                user_uid = ($(this).parent().attr('id')).split("-");
                                                                //XMPPDebug.log(user_uid[1]);
                                                                UserOperations.delete_user(user_uid[1]);
                                                            }
                                                        });
                                                        UserOperations.search_last_users();
                                                        $("#check_all").attr('checked', false);
                                                        $(this).dialog("close");
                                                    }
                                                }
            });
		});
    },
    update_loading: function() {
        console.log(USER_GUI.no_delete_users);
        if (USER_GUI.no_delete_users == 0) {
            $('#remove_selected_items img').hide();
        }
    },
    on_create: function(){
        var uploader = new qq.FileUploader({
            element: document.getElementById('user_file_uploader'),
            action: 'php/common/php.php',
            debug: true,
            multiple: false,
            allowedExtensions: ['txt'],
            onComplete: function(id, file, response) {
                USER_GUI.batch_user_file = file;
                $('#file_uploader').attr('disabled', true);
                $('#file_uploader').parent().hide();
                $('#user_delete_file').show();
                USER_GUI.response_batch_users = response.elements;
            }
        });
        USER_GUI.create_user_bubble_info('.user_img_quota');
        USER_GUI.create_user_bubble_info('.user_img_course');
        USER_GUI.create_user_bubble_info('.user_img_profile');
    }

}

/**
 *	Manejadores de eventos más comunes
 */
$(document).ready(function(){
	/**
	 *	Eliminación de usuarios. En el click se pedirá confirmación, y en caso afirmativo se procederá a la eliminación del user
	 *	<a class="action del" href="" uid="UID_USER">...</a>
	 */
	$(GUI.main_frm).delegate('a.user_del_icon','click', function(event){
		event.preventDefault();
        var user = $(this).attr('uid');
        $.get('php/user/_del_user.php',{user: user}, function(data){
			$('#del_dialog').html(data).dialog({height: 120,
                                                title: _translate('Delete user'),
                                                resizable: false,
                                                modal: true,
                                                buttons: {
                                                    "Cancelar": function() {$(this).dialog("close");},
                                                    "Eliminar": function() {UserOperations.delete_user(user);UserOperations.search_last_users();$(this).dialog("close");}
                                                    }
                                                });
		});
	});

    /**
	 *	Eliminación de usuarios. En el click se pedirá confirmación, y en caso afirmativo se procederá a la eliminación del user
	 *	<a class="action del" href="" uid="UID_USER">...</a>
	 */
	$(GUI.main_frm).delegate('a.user_edit_icon','click', function(event){
		event.preventDefault();
        var user = null;
        var user_uid = $(this).attr('uid');
        var keys = Object.keys(USER_GUI.last_data_search.data);
        var values = []
        for(var i = 0; i < keys.length; i++) {
            var key = keys[i];
            values[i] = USER_GUI.last_data_search.data[key];
            if (user_uid == values[i].uid) {
                user = values[i];
            }   
        }

        if (user.profile == 'Fijo') {
            user.profile = 1;
        } else {
            user.profile = 2;
        }

        if (user.group == 'A') {
            user.group = 1;
        } else {
            if (user.group == 'G') {
                user.group = 2;
            } else {
                user.group = 3;
            }
        }
        
        $.post('php/user/_edit_user.php',{user: user}, function(data){
			$('#edit_dialog').html(data).dialog({width: 500,
                                                height: 560,
                                                title: _translate('Update user'),
                                                resizable: false,
                                                modal: true,
                                                buttons: {
                                                    "Cancelar": function() {$(this).dialog("close");},
                                                    "Actualizar": function() {
                                                                    if (UserOperations.edit_user()){
                                                                        UserOperations.search_last_users();
                                                                        $(this).dialog("close");
                                                                    }
                                                                  }
                                                }
                                            });
            USER_GUI.create_user_bubble_info('.user_img_quota_edit');
            USER_GUI.create_user_bubble_info('.user_img_course_edit');
            USER_GUI.create_user_bubble_info('.user_img_profile_edit');
        });
    });
});