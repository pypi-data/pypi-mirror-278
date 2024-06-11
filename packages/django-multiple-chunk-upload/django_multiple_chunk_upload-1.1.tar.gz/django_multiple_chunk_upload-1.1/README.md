Django multiple chunks uploads
==============================

Upload in blocks of multiple files and with progress bar

Demo
----

Add app in settings

.. code:: python

     INSTALLED_APPS = (
       # ...
       'django_multiple_chunk_upload',
   )

Define MAX_BYTES in settings

.. code:: python

     MAX_BYTES = 1000000000 #1tb

Include JS in HTML

.. code:: html

     <script src="{% static 'django_multiple_chunk_upload/js/chunk_upload.js' %}"></script>

Call send_file functions with params

.. code:: html

     <button class="btn btn-success" id="upload-button" onclick="send_file(['input_file1'], ['non_input_file1'],'{% url 'chunk_upload' %}', '{% url 'complete_upload' %}', '{% url 'redirect_url' %}')">Upload</button>

Create a progress bar

.. code:: html

   <div class="progress"
           role="progressbar"
           aria-label="Example with label"
           aria-valuenow="25"
           aria-valuemin="0"
           aria-valuemax="100">
       <div id="progress-bar" class="progress-bar" style="width: 0%">0%</div>
   </div>

Create a message div

.. code:: html

   <div id="message-upload" class="alert alert-primary" role="alert">
               
   </div>

Exemple usage models and views
------------------------------

Create a model extends ChunkUpload

.. code:: python

   class MyModel(ChunkUpload):
       nome_completo = models.CharField(max_length=256, null=True, blank=True)
       file1 = models.FileField(upload_to="chunk_upload", null=True, blank=True)
       file2 = models.FileField(upload_to="chunk_upload", null=True, blank=True)

Create a view handle Upload

.. code:: python

   @method_decorator([csrf_exempt], name='dispatch')
   class MyView1(View, UploadMixin):
       MODEL_CLASS = MyModel
       FILE_FIELDS = ['file1', 'file2']
       UPLOAD_TO = 'chunk_uploads'

       def post(self, request):
           
           return self.handle_chunk_upload(
               request, self.FILE_FIELDS, self.MODEL_CLASS, self.UPLOAD_TO
           )

Create a complete upload View

.. code:: python

   @method_decorator([csrf_exempt], name='dispatch')
   class CompleteUpload(View, CompleteUploadMixin):
       MODEL_CLASS = MyModel
       NON_FILE_FIELDS = ['nome_completo',]

       def post(self, request):
           return self.handle_complete_upload(
               request, self.NON_FILE_FIELDS, self.MODEL_CLASS
           )