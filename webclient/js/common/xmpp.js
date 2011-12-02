var XMPP = {

	SERVER_NAME		: 'winterfall.local',
	SERVER_BOSCH    : 'http://winterfall.local/http-bind',
	G3_XMLNS		: 'cga:gesuser3:',
	RESOURCE		: 'GESUSER_Client',
	connection      : null,
	jid             : null,
	user			: null,
	pass			: null,
	
	/**
	 * Crea una stanza IQ a partir de los datos sacados del formulario (recogidos como parámetros)
	 */
	send_iq: function(fields, data){
		
		var iq = $iq({to: data.etq+'@'+XMPP.SERVER_NAME+'/'+XMPP.RESOURCE, type:data.type})
					.c(data.etq, {xmlns: XMPP.G3_XMLNS+data.etq, action:data.action});

		$.each(fields, function (i, field){
			if(field.op){
				iq.c(field.name,{op: field.op}).t(field.value).up();
			}else{
                console.log(field.name + ":" + field.value);
				iq.c(field.name).t(field.value).up();
			}
		});
        //console.log(iq.toString());
        XMPPDebug.log(iq.toString());
		console.info(iq.toString());
		//TODO: activar!
		return XMPP.connection.sendIQ(iq);
	},
    /*send_batch_iq: function(fields, data){

		var iq = $iq({to: data.etq+'@'+XMPP.SERVER_NAME+'/'+XMPP.RESOURCE, type:data.type})
					.c(data.etq, {xmlns: XMPP.G3_XMLNS+data.etq, action:data.action});

		$.each(fields, function (i, field){
            iq.c(field.name);
            $.each(field.value, function (e, f) {
                iq.c(f.name).t(f.value).up();
            });
        });

        //console.log(iq.toString());
        XMPPDebug.log(iq.toString());
		//console.info(iq.toString());
		//TODO: activar!
		//XMPP.connection.sendIQ(iq);
	},*/

	/**
	 *	Cuando se recibe una <presence> se activa/desactiva el módulo correspondiente
	 */
	on_presence: function (presence) {
        var from = $(presence).attr('from');
		var type = $(presence).attr('type');
        /*var barejidfrom = Strophe.getBareJidFromJid(from);
		var resource = Strophe.getResourceFromJid(from);*/

		var array = from.split('@');
		var module = array[0];

		if(XMPP.user != module){ //comprobar que la presencia no es del usuario (mi presence)
			//Habilitar/Deshabilitar módulo en función del type

			if(type=='unavailable'){
				GUI.module_off(module);
			}else{
				GUI.module_on(module);
			}
		}		
		return true;
    },

	/**
	 *	Cuando se recibe una iq hay que ver de qué type es, en caso de error informamos de tal, en caso de result
	 *	hay que verificar si ha ocurrido algún error e informar de él o de informar del resultado de la operación
	 *	que indica la <iq> en el action (en este caso si la acción recibida se corresponde con la sección activa
	 *	en la GUI reiniciamos el formulario)
	 *
	 *	En el caso de tener elementos <item> en un type=result hay que imprimir esos items en la interfaz
	 */
    on_iq: function (iq) {
		var type = $(iq).attr('type');
		var id = $(iq).attr('id');
        var a_t = $(iq).attr('action').split(':');
		var action = a_t[0];
        var task = a_t[1];
        //console.log(action);
        //console.log(task);

		var from = $(iq).attr('from');
		var array_from = from.split('@');
		var module = array_from[0];

		var section = module+'-'+action;

        if (USER_GUI.iq_list_id) {
            $.each(USER_GUI.iq_list_id, function() {
                if (this.id == id){
                    this.result = type;
                    if (this.result == 'result') {
                        if ($(iq).children('error').attr('code')) {
                            this.result = 'error';
                        }
                    }
                    UserOperations.update_log_system(id);
                }
            });
        }

        if (task == "delete") {
            USER_GUI.no_delete_users -= 1;
            UserOperations.update_loading();
        }

		if(type==='error'){ // error en el servidor
			var error = $(iq).find('error');
			//var code = error.attr('code');
			var error_text = error.text();
			GUI.msg('error', error_text);
		}
		else if(type==='result'){
			var error = $(iq).find('error');
			var error_text = error.text();
			if(error_text){
				GUI.msg('error', action+': '+error_text);
			}else{ 
				GUI.msg('completed', action + ':' + task + ': success');
				if(Common.get_section_active() == section){
					//TODO decidir esto
					//$(GUI.main_frm).reset();
				}

				// Tenemos items en el caso de un action=read type=result
                var response = $(iq).find("response");
                if (response.length > 0) {
                    var items = $(iq).find("item");
                    if (items.length > 0) {
                        var array = [];
                        /*$(GUI.users_table+' tbody').fadeOut("slow", function () {
                            $(GUI.users_table+' tbody').remove();
                        });*/
                        var pair = true;
                        $(iq).find("item").each(function () {
                            pair = !pair;
                            var uid = $(this).find('uid').text();
                            XMPPDebug.log(uid);
                            var gecos = $(this).find('gecos').text();
                            var quota = $(this).find('quota').text();
                            var course = $(this).find('course').text();
                            var group = $(this).find('group').text();
                            var profile = $(this).find('profile').text();

                            //GUI.print_user_result({uid: uid, gecos: gecos, quota: quota, course: course, group: group, profile: profile, pair: pair});
                            array.push({uid: uid, gecos: gecos, quota: quota, course: course, group: group, profile: profile, pair: pair});

                        });
                        var o = {data: array};
                        UserOperations.print_user_result(o);
                    } else {
                        UserOperations.print_user_result({error: "error"});
                    }
                }
			}
		}

		return true;
    }
}

/**
 *	Conectar al sistema. Realiza la conexión XMPP con el servidor ejabberd
 *	El password ha de venir de la siguiente manera: '{SHA}'+sha1(pass_plano)
 */
$(document).bind('connect', function (ev, data) {
	GUI.loading(_translate('loading'));
	GUI.loading(_translate('connecting to the system'));
	
	var conn = new Strophe.Connection(XMPP.SERVER_BOSCH);

	//TODO desactivar debug
	//////////DEBUG
	conn.xmlInput = function (body) {
		XMPPDebug.show_traffic(body, 'incoming');
	};
	conn.xmlOutput = function (body) {
		XMPPDebug.show_traffic(body, 'outgoing');
	};
	//////////DEBUG

	var jid = data.user+'@'+XMPP.SERVER_NAME+'/GESUSER_Client';

	GUI.msg('process','connecting to the system');
	conn.connect(jid, data.password, function (status) {
		
		if (status === Strophe.Status.CONNECTED) {
			$(document).trigger('connected');
		} else if (status === Strophe.Status.DISCONNECTED) {
			$(document).trigger('disconnected');
		} else if (status === Strophe.Status.AUTHFAIL) {
			$(document).trigger('disconnected');
		}
	});

	XMPP.jid = jid;
	XMPP.user = data.user;
	XMPP.pass = data.password;
	XMPP.connection = conn;
});

/**
 *	Desconexión del sistema. Desconecta la conexión XMPP
 *	El método de desconexión lanza el evento disconnected
 */
$(document).bind('disconnect', function(ev, data){
	GUI.msg('process',_translate('disconnecting'));
	XMPP.connection.disconnect();
	$.post('php/session/session.php',
			{action:'destroy'},
			function(data){
				var jsonData = jQuery.parseJSON(data);

				if(!jsonData.ok){
					GUI.msg('error', _translate('there is an error with the session')+', '+_translate('please contact your admin'));
				}
			}
	);
});

/**
 * Cuando se recibe el evento 'conectado' se añaden manejadores a las presence y las iq,
 * se establece la sesión php y los elementos iniciales del sistema
 */
$(document).bind('connected', function(){
	//TODO: eliminar esto
	//GUI.module_on('user');
	GUI.msg('completed','connected to the system');

	//Añadimos manejadores
	XMPP.connection.addHandler(XMPP.on_presence,null, "presence");
    XMPP.connection.addHandler(XMPP.on_iq,null, "iq");

	XMPP.connection.send($pres());

	$.post('php/session/session.php',
			{user:XMPP.user, pass:XMPP.pass, action:'start'},
			function(data){
				var jsonData = jQuery.parseJSON(data);

				if(!jsonData.ok){
					GUI.msg('error', _translate('there is an error with the session')+', '+_translate('please contact your admin'));
				}
			}
	);	
	GUI.unloading();
	GUI.welcome();
});

$(document).bind('disconnected', function(){
	GUI.unloading();
	GUI.go_login();
	GUI.modules_off();
	GUI.msg('completed','disconnected');	
});