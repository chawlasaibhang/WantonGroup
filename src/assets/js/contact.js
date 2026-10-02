/* Contact form: sends the enquiry by WhatsApp or email. No backend needed. */
(function () {
  var form = document.getElementById('enquiryForm');
  if (!form) return;
  var error = document.getElementById('formError');
  var NUMBERS = { 'Ajuni Luxe': '919321215812' };
  var DEFAULT_NUMBER = '919867939177';

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var via = (e.submitter && e.submitter.value) || 'whatsapp';
    var get = function (id) { return document.getElementById(id).value.trim(); };
    var type = get('enquiryType'), name = get('cName'), email = get('cEmail');
    var phone = get('cPhone'), company = get('cCompany'), message = get('cMessage');

    var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!name || !emailOk || !message) {
      error.hidden = false;
      (!name ? document.getElementById('cName') : !emailOk ? document.getElementById('cEmail') : document.getElementById('cMessage')).focus();
      return;
    }
    error.hidden = true;

    var lines = [
      'Enquiry: ' + type,
      'Name: ' + name,
      'Email: ' + email,
      phone && 'Phone: ' + phone,
      company && 'Company: ' + company,
      '',
      message
    ].filter(function (l) { return l !== false && l !== ''; });

    if (via === 'email') {
      var subject = encodeURIComponent('Wanton Group enquiry: ' + type);
      window.location.href = 'mailto:info@wantongroup.com?subject=' + subject + '&body=' + encodeURIComponent(lines.join('\n'));
    } else {
      var number = NUMBERS[type] || DEFAULT_NUMBER;
      window.open('https://wa.me/' + number + '?text=' + encodeURIComponent('Hi, ' + lines.join('\n')), '_blank', 'noopener');
    }
  });
})();
