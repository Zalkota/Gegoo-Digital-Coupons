module.exports = function(grunt) {
	grunt.initConfig({
	  sass: {
	    dev: {
	      src: ['mysite/static/sass/_video.scss'],
	      dest: 'mysite/static/css/grunt.css',
	    },
	  },
	  watch: {
	    sass: {
	      files: ['mysite/static/sass/*.scss'],
	      tasks: ['sass'],
	    },
	    livereload: {
	      options: { livereload: true },
	      files: ['mysite/**/*'],
	    },
	  },
	});
	grunt.loadNpmTasks('grunt-contrib-sass');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.registerTask('default',['watch']);
}
