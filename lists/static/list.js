window.Superlists = {}
console.log('js loaded');
window.Superlists.initialize = function(){
    $('input[name="text"]').on('keypress', function(){
        console.log('js called');
        $('.has-error').hide();
    });
};