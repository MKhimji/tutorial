/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
    config.extraPlugins = 'ckeditor-gwf-plugin,codemirror,sourcedialog,codesnippet,lineutils,widget';
	config.font_names = 'GoogleWebFonts;' + 'Geo; Montserrat; Times New Roman;Verdana';
	config.codeSnippet_theme = 'github';
	config.contentsCss = '/static/accounts/blog.css';
	//CKEDITOR.config.enterMode = CKEDITOR.ENTER_BR;

	//CKEDITOR.config.insertpre_class = 'prettyprint';
	// CKEDITOR.config.insertpre_style = 'background-color:#F8F8F8;border:1px solid #DDD;padding:2px;';
	

	
	
	
};
