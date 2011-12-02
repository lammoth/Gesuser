jQuery.fn.reset = function () {
  $(this).each (function() {this.reset();});
}

/**
 *	Este archivo engloba las operaciones más comunes e independientes de las clases específicas:
 *		1- Clase Fechas: operaciones de fechas y horas
 *		2- Clase GUI: operaciones a nivel de interfaz
 *		3- Manejadores de los eventos más comunes, como son los "click" y los "submit" de los formularios
 */

var GUI = {
	//constantes: elementos de la interfaz
	content: '#center_section',
	submenu: '#left_section',
	main_frm: '#main_frm',
	login_frm: '#login_frm',
	section_title: '#section_tit',
	main_menu: '#left_sec_main',
	global_menu: '#main_sections',
	
    events_list: '#right_section',
    
    last_msg_date: null,
    last_msg: null,
    iq_list_id: [],
    actual_module: null,
    
    
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

	set_main_frm: function(titulo, html){
        $('#start').hide();
        $(this.section_title).html(titulo);
        $(this.main_frm).html(html);
		/*if(titulo!='Inicio'){
            $('#start').hide();
            $(this.section_title).html(titulo);
            $(this.main_frm).html(html);
        } else {
            $(this.section_title).html(titulo);
        }*/
	},

	set_sub_menu: function(html){
		$(this.submenu).html(html);
	},

	/**
	 *	Muestra el Growl y añade el mensaje a los eventos
	 *	El mensaje ha de venir sin traducir
	 */

	msg: function(status, msg){
        var now = new Date();
        var seconds = now.getSeconds();
        //console.log(seconds);

        if (msg != GUI.last_msg) {
            GUI.show_msg(status, msg);
            GUI.last_msg = msg;
        } else {
            if (!GUI.last_msg_date) {
                GUI.show_msg(status, msg);
                GUI.last_msg_date = seconds;
                GUI.last_msg = msg;
            } else {
                if (seconds > GUI.last_msg_date + 10 || seconds < GUI.last_msg_date) {
                    GUI.show_msg(status, msg);
                    GUI.last_msg_date = seconds;
                    GUI.last_msg = msg;
                }
            }
        }
	},
    show_msg: function(status, msg){
        if(status != ''){
            msg = _translate(msg);

            $.Growl.show(msg, {icon: status});
            var texto = _translate(status);

            var fecha = new Dates();
            $('#events').prepend('<li><span class="time">'+fecha.get_Date()+'<br /></span><span class="event_'+status+'">'+texto+'</span><span>'+msg+'</span></li>')

            if($('#events li').length > 5){
                $('#events li:last-child').remove();
                $('#events li:last-child').css({'border': '0'});
            } else {
                $('#events li:last-child').css({'border': '0'});
            }
        }
    },
	module_on: function(module){
		this.msg('completed',_translate('module activated')+': '+_translate(module));
		$('#module-'+module).removeClass('inactive').addClass('active');
        if ($('#module-'+module).HasBubblePopup()) {
            $('#module-'+module).RemoveBubblePopup();
        }
	},
	module_off: function(module){
		this.msg('error',_translate('module deactivated')+': '+_translate(module));
		$('#module-'+module).removeClass('active').removeClass('selected').addClass('inactive');
        if (!$('#module-'+module).HasBubblePopup()) {
            $('#module-'+module).CreateBubblePopup(GUI.options_bubble);
        }
        console.log("actual:" + GUI.actual_module);
        console.log("disabled:" + ("module-" + module));
        if (GUI.actual_module == ("module-" + module)){
            GUI.welcome();
        }
	},
	modules_off: function(){
		$(GUI.main_menu+' li.active').removeClass('active').addClass('inactive');
		$(GUI.main_menu+' li.selected').removeClass('selected').addClass('inactive');
		GUI.msg('completed',_translate('modules deactivated'));
	},
	loading: function(msg){
		$('#content_center_section div').hide();
		$('#loading-text').html(msg);
		$('#loading').show();
	},
	unloading: function(){
		$('#content_center_section div').show();
		$('#loading').hide();
	},
	welcome: function(){
        $('#header_center_section').removeClass('head_center_section_login').addClass('head_center_section_normal');
		$.get('php/home/welcome.php',{user: XMPP.user}, function(data){
            GUI.actual_module = "module-home";
			//$('#start').html(data);
            $('#start').html('');
			$('#start').show();
			$.get('common/menu.php', function(data){
				$('#header').html(data);
                // When login in the system, section "home" is selected
                $('#module-home').removeClass('inactive').addClass('selected');
                $('li.inactive').CreateBubblePopup(GUI.options_bubble);
			});
			$('#user_name').html(XMPP.user);
            $(GUI.events_list).show();
            Common.show_welcome_menu();
		});
	},
	go_login: function(){
        $(".ui-dialog-content").dialog("close");
        $(GUI.section_title).html(function() {
            return 'Bienvenido a g3suser';
        });
		$.get('php/common/login_form.php', function(data){
            $('#header_center_section').removeClass('head_center_section_normal').addClass('head_center_section_login');
            $(GUI.events_list).hide();
			$('#start').html(data);
			$('#start').show();			
			$('#header').html('');
			//$('#right_section').html('');
			$(GUI.main_frm).html('');
			$(GUI.submenu).html('');
		});
	},
	set_error_form: function(id, msg){
		$('#'+id).parent().parent().find('span.error').html(msg);
	},
	clean_error_form: function(id){
		GUI.set_error_form(id, '');
	}
}

/**
 *	Operaciones comunes de fecha y hora
 */
var Dates = function(){
	this.days = new Array(_translate("Sunday"),_translate("Monday"),_translate("Tuesday"),_translate("Wenesday"),_translate("Thursday"),
                          _translate("Friday"),_translate("Saturday"));

	Dates.prototype.get_Date = function(){
		var now = new Date();
		return this.days[now.getDay()]+" "+now.getDate()+", "+now.getHours()+":"+now.getMinutes();
	}
}

var Global = {
	id_usuario: null
}

var Common = {
    stanza_sended : null,

	logout: function(){
		$(document).trigger('disconnect');
	},
	session_renove: function(){
		$.post('php/session/session.php',
			{action:'renove'},
			function(data){				
			}
		);
	},
	validate_form: function(jq_form){

		var errors = false;
		$.each(jQuery(':input:not(input[type=button])',jq_form), function(){
			var error_elem = false;
			if($(this).attr('required')){ 
				if(!$(this).val()){
					errors = true;
					error_elem = true;
					GUI.set_error_form($(this).attr('id'), _translate('field required'));
				}else{
					GUI.clean_error_form($(this).attr('id'));
				}
			}
			if($(this).attr('integer') && !error_elem){
				if(isNaN($(this).val())){
					errors = true;
					GUI.set_error_form($(this).attr('id'),_translate('this value must be integer'));
				}else{
					GUI.clean_error_form($(this).attr('id'));
				}
			}
            if($(this).attr('filtered') && !error_elem){
                var filter = /[^A-Za-z0-9]/;
                if(filter.test($(this).val())){
					errors = true;
					GUI.set_error_form($(this).attr('id'),_translate('this value is not allowed'));
				}else{
					GUI.clean_error_form($(this).attr('id'));
				}
			}
            if($(this).attr('lessfiltered') && !error_elem){
                var filter = /[^A-Za-z0-9.º ]/;
                if(filter.test($(this).val())){
					errors = true;
					GUI.set_error_form($(this).attr('id'),_translate('this value is not allowed'));
				}else{
					GUI.clean_error_form($(this).attr('id'));
				}
			}
		});

		//comprobación de elemenos password
		var pass_anterior = null;
		$.each(jQuery(':input[type=password]', jq_form), function(){
			if(pass_anterior == null){
				pass_anterior = $(this).val();
			}
			else{
				if($(this).val() != pass_anterior){
					errors = true;
					GUI.set_error_form($(this).attr('id'),_translate('password doesn\'t match'));
				}else{
					GUI.clean_error_form($(this).attr('id'));
				}
			}
		});

		return errors;
	},

	get_section_active: function(){
		return $('li.section_active a').attr('module')+'-'+$('li.section_active a').attr('href');
	},

    show_welcome_menu: function(){
        var obj = $(this);
		var url = 'php/home/submenu.php';

        $.get(url, function(data){
            GUI.set_sub_menu(data);

            //reestablecemos las clases css
            //$(GUI.main_menu+' li.selected').removeClass('selected').addClass('active');
            //obj.parent().removeClass('active').addClass('selected');

            $(GUI.submenu).show();
            $(GUI.submenu+' li.section_active a').click();
            Common.session_renove();
        });
    }
}

/**
 *	Manejadores de eventos más comunes
 */
$(document).ready(function(){
	$.post('php/session/session.php',
			{action:'check'},
			function(data){
				var jsonData = jQuery.parseJSON(data);

				if(jsonData.exists){
					$(document).trigger('connect', {user: jsonData.user, password: jsonData.pass});
				}
			}
	);

	/**
	 *	Cargar elementos que no forman parte de ningún módulo específico (como la configuración)
	 *	Estos elementos forman parte de la cabecera (#header), son <a> con class=simple_load:
	 *		--> <a class="simple_load" href="script">
	 *
	 *	El título del elemento a cargar se encuentra en el <span> que se encuntra dentro, y el script
	 *	que se ha de cargar se encuentra en
	 *	'php/common/[HREF]'
	 *
	 *	Una vez cargado el elemento por AJAX se estable en el contenido principal
	 */
	$('#header').delegate('a.simple_load','click',function(event){
		event.preventDefault();
		var titulo = $(this).find('span').html();
		var url = 'php/common/'+$(this).attr('href')+'.php';
        $('#' + GUI.actual_module).removeClass('selected').addClass('active');


		$.get(url, function(data){
			//no hay submenú, por lo que limpiamos esa zona
			$(GUI.submenu).html('');
            
			GUI.set_main_frm(titulo, data);
			Common.session_renove();
		});
	});

    $('#header').delegate('a.important_link','click',function(event){
		event.preventDefault();
		Common.logout();
	});

	/**
	 * Cargar módulo al hacer click en el elemento del menú (no inactivo)
	 *
	 * El elemento href del <a> contiene el nombre del script del menú a cargar mediante AJAX.
	 * Ej: href="users" => php/menus/users.php	 
	 *
	 * Por último realizamos operaciones de interfaz y cargamos el primer elemento del menú
	 */
	$('#header').delegate('a.main_menu', 'click', function(event){
		event.preventDefault();
       
		// Continuamos si el módulo no está inactivo y seleccionado
		if(!$(this).parent().hasClass('inactive') || $(this).parent().hasClass('selected')){
            GUI.actual_module = "module-" + $(this).attr('href');
			var obj = $(this);
			var url = 'php/'+$(this).attr('href')+'/submenu.php';

			$.get(url, function(data){
				GUI.set_sub_menu(data);
				
				//reestablecemos las clases css
				$(GUI.main_menu+' li.selected').removeClass('selected').addClass('active');
				obj.parent().removeClass('active').addClass('selected');

				$(GUI.submenu).show();
				$(GUI.submenu+' li.section_active a').click();
				Common.session_renove();
			});
		}
	});

	/**
	 *	Cargar submódulo al hacer click en un elemento del submenú
	 *		--> <li><a class="click" module="modulo" href="script">
	 *	La url a cargar se encuentra en 'php/ATRIBUTO_MODULE/ATRIBUTO_HREF.php'
	 */
	$(GUI.submenu).delegate('li a', 'click', function (event){
		event.preventDefault();
		var obj = $(this);
		var titulo = $(this).find('span').html();
		var modulo = $(this).attr('module');
		var script = $(this).attr('href')+'.php';
        var action = $(this).attr('href');
		var url = 'php/'+modulo+'/'+script;

		$.get(url, {user: XMPP.user}, function(data){
			GUI.set_main_frm(titulo, data);
            var method = (modulo.charAt(0).toUpperCase() + modulo.slice(1)) + 'Operations.on_' + action;
            try {
                eval(method + '();');
            } catch(e) {
                console.log(e);
            }
			//reestablecemos las clases css
			$(GUI.submenu+' li.section_active').removeClass('section_active');
			obj.parent().addClass('section_active');
			Common.session_renove();
		});		
	});

	/**
	 * Submit del formulario principal
	 * A partir de los elementos del formulario crea la stanza a enviar al servidor xmpp
	 */
	$(GUI.main_frm).submit(function(event){
		event.preventDefault();

		var submit = $(this).find('input[type=submit]');
		var fields = $(this).serializeArray();

		var etq = submit.attr('etq');
		var type = submit.attr('stanza_type');
		var action = submit.attr('action');

		XMPP.send_iq(fields, {etq:etq, type:type, action:action});
		Common.session_renove();
	});

	/**
     * Formulario de login
     * Llama por AJAX al archivo de login que mira las credenciales del usuario y crea la sesión php
     * Si todo va bien modifica la variable global ID_USUARIO utilizada en la aplicación y va al inicio de la aplicación
     */
    $('#start').delegate(GUI.login_frm,'submit',function(event){
		event.preventDefault();
        var user = $('#user').val();

		//TODO: activar sha1
        //var pass = hex_sha1($('#pass').val());
		var pass = $('#pass').val();

		$(document).trigger('connect', {user: user, password: pass});
    });
});