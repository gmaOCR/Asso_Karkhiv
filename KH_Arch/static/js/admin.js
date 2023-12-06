
document.addEventListener('DOMContentLoaded', function() {
    const contentTypeSelect = document.querySelector('#id_content_type');
    const objectIdSelect = document.querySelector('#id_object_id');

    contentTypeSelect.addEventListener('change', function() {
        const contentTypeId = this.value;

        fetch(`/get-content-objects/?content_type_id=${contentTypeId}`)
            .then(response => response.json())
            .then(data => {
                objectIdSelect.innerHTML = '';  // Clear current options
                data.objects.forEach(function(item) {
                    const option = new Option(item.name, item.id);
                    objectIdSelect.add(option);
                });
            })
            .catch(error => console.error('Error:', error));
    });
});
