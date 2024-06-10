#ifndef BASE64_H
#define BASE64_H
typedef struct {
	PyObject_HEAD
		unsigned char* data;//明文
	unsigned int* source_bytes;//明文字节
	unsigned int* executed_bytes;//密文字节
	unsigned char* encrypted_data;//密文
}Base64block;
static void Base64Block_destroy(Base64block* self)
{
	Py_TYPE(self)->tp_free(self);
}
static PyObject* Base64Block_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
	Base64block* self = (Base64block*)type->tp_alloc(type, 0);
	if (self == NULL)
	{
		return NULL;
	}
	else
	{
		self->data = NULL;
		self->encrypted_data = NULL;
		self->executed_bytes = NULL;
		self->source_bytes = NULL;
		Py_XINCREF(self);
		return self;
	}
}
static int Base64Block_init(Base64block* self, PyObject* args, PyObject* kwds)
{
	return 0;
}
static PyMemberDef Base64Block_members[] = {
	{NULL}
};
static PyObject* Base64Encryptor(Base64block* self, PyObject* args)
{
	unsigned char base64_box[] = {
	'A','B','C','D','E','F','G','H',
	'I','J','K','L','M','N','O','P',
	'Q','R','S','T','U','V','W','X',
	'Y','Z','a','b','c','d','e','f',
	'g','h','i','j','k','l','m','n',
	'o','p','q','r','s','t','u','v',
	'w','x','y','z','0','1','2','3',
	'4','5','6','7','8','9','+','/'
	};
	unsigned char* data;
	if (PyArg_ParseTuple(args, "y", &data) < 0)
	{
		Py_RETURN_NONE;
	}
	else
	{
		self->data = (unsigned char*)malloc(sizeof(unsigned char) * strlen(data));
		int counter = 0;
		while (counter < strlen(data))
		{
			self->data[counter] = data[counter];
			counter++;
		}
		self->data[counter] = '\0';
		self->source_bytes = (unsigned int*)malloc(sizeof(unsigned int) * strlen(data) * 4);
		counter = 0;
		for (int i = 0; i < strlen(data); i++)
		{
			unsigned int high_4bit = self->data[i] >> 4;
			unsigned int low_4bit = self->data[i] & 0xf;
			unsigned int high_high_2bit = high_4bit >> 2;
			unsigned int high_low_2bit = high_4bit & 0x3;
			unsigned int low_high_2bit = low_4bit >> 2;
			unsigned int low_low_2bit = low_4bit & 0x3;
			self->source_bytes[counter++] = high_high_2bit;
			self->source_bytes[counter++] = high_low_2bit;
			self->source_bytes[counter++] = low_high_2bit;
			self->source_bytes[counter++] = low_low_2bit;
		}
		int padding = counter % 3;
		if (padding != 0)
		{
			for (int i = 0; i < 3 - padding; i++)
			{
				self->source_bytes[counter++] = 0x0;
			}
		}
		int length = counter / 3;
		self->executed_bytes = (unsigned int*)malloc(sizeof(unsigned int) * length);
		for (int i = 0; i < length; i++)
		{
			unsigned int front = self->source_bytes[i * 3];
			unsigned int middle = self->source_bytes[i * 3 + 1];
			unsigned int rear = self->source_bytes[i * 3 + 2];
			int temp = ((front & 0xf) << 4) | (middle & 0xf) << 2 | (rear & 0xf);
			self->executed_bytes[i] = temp;
		}
		self->encrypted_data = (unsigned char*)malloc(sizeof(unsigned char) * length);
		for (int i = 0; i < length; i++)
		{
			self->encrypted_data[i] = base64_box[self->executed_bytes[i]];
		}
		self->encrypted_data[length] = '\0';
		PyObject* result = Py_BuildValue("y", self->encrypted_data);
		Py_INCREF(result);
		return result;
	}
}
static PyObject* Base64Decryptor(Base64block*self,PyObject*args)
{
	unsigned char base64_box[] = {
	'A','B','C','D','E','F','G','H',
	'I','J','K','L','M','N','O','P',
	'Q','R','S','T','U','V','W','X',
	'Y','Z','a','b','c','d','e','f',
	'g','h','i','j','k','l','m','n',
	'o','p','q','r','s','t','u','v',
	'w','x','y','z','0','1','2','3',
	'4','5','6','7','8','9','+','/'
	};
	unsigned char* en_data;
	if (PyArg_ParseTuple(args, "y", &en_data) < 0)
	{
		Py_RETURN_NONE;
	}
	else
	{
		self->encrypted_data = (unsigned char*)malloc(sizeof(unsigned char)*strlen(en_data));
		for (int i = 0; i < strlen(en_data); i++)
		{
			self->encrypted_data[i] = en_data[i];
		}
		self->encrypted_data[strlen(en_data)]='\0';
		self->executed_bytes = (unsigned int*)malloc(sizeof(unsigned int)*strlen(en_data));
		int counter = 0;
		for (int i = 0; i < strlen(en_data); i++)
		{
			int index = 0;
			while (index < 64)
			{
				if (base64_box[index] == self->encrypted_data[i])
				{
					break;
				}
				index++;
			}
			self->executed_bytes[i] = index;
		}
		self->source_bytes = (unsigned int*)malloc(sizeof(unsigned int)*strlen(en_data)*3);
		for (int i = 0; i < strlen(en_data); i++)
		{
			unsigned int get = self->executed_bytes[i];
			unsigned int front = (get & 0x30) >> 0x4;
			unsigned int middle = (get & 0xc) >> 0x2;
			unsigned int rear = get & 0x3;
			self->source_bytes[counter++] = front;
			self->source_bytes[counter++] = middle;
			self->source_bytes[counter++] = rear;
		}
		int length = counter/ 4;
		self->data = (unsigned char*)malloc(sizeof(unsigned char)*length);
		counter=0;
		for (int i = 0; i < length; i++)
		{
			unsigned int bit_4 = self->source_bytes[i * 4] << 6;
			unsigned int bit_3 = self->source_bytes[i * 4 + 1] << 4;
			unsigned int bit_2 = self->source_bytes[i * 4 + 2] << 2;
			unsigned int bit_1 = self->source_bytes[i * 4 + 3];
			unsigned int temp = bit_4 | bit_3 | bit_2 | bit_1;
			if(temp==0)
			{
			    self->data[i]=0;
			}
			self->data[counter++] = temp;
		}
		self->data[counter] = '\0';
		PyObject* result = Py_BuildValue("y",self->data);
		Py_INCREF(result);
		return result;
	}
}
static PyObject* GetEncryptData(Base64block* self)
{
	PyObject* result = Py_BuildValue("y", self->encrypted_data);
	Py_INCREF(result);
	return result;
}
static PyObject* GetData(Base64block* self)
{
	PyObject* result = Py_BuildValue("y",self->data);
	Py_INCREF(result);
	return result;
}
static PyObject* DestroyBase64Block(Base64block* self)
{
	free(self->data);
	free(self->encrypted_data);
	free(self->executed_bytes);
	free(self->source_bytes);
	Py_RETURN_NONE;
}
static PyMethodDef Base64block_methods[] = {
	{"destroy_base64",(PyCFunction)(PyObject * (*)(Base64block*))DestroyBase64Block,METH_NOARGS,""},
	{"Base64Encryptor",Base64Encryptor,METH_VARARGS,""},
	{"Base64Decryptor",Base64Decryptor,METH_VARARGS,""},
	{"get_encrypt_data",(PyCFunction)(PyObject * (*)(Base64block*))GetEncryptData,METH_NOARGS,""},
	{"get_data",(PyCFunction)(PyObject * (*)(Base64block*))GetData,METH_NOARGS,""},
	{NULL}
};
static PyTypeObject Base64block_object = {
	PyVarObject_HEAD_INIT(NULL,0)
	.tp_name = "Base64Utility.Base64Block",
	.tp_new = Base64Block_new,
	.tp_dealloc = (destructor)Base64Block_destroy,
	.tp_init = (initproc)Base64Block_init,
	.tp_members = Base64Block_members,
	.tp_methods = Base64block_methods,
	.tp_basicsize = sizeof(Base64block),
	.tp_itemsize = 0,
	.tp_flags = Py_TPFLAGS_BASETYPE | Py_TPFLAGS_DEFAULT
};
#endif // !BASE64_H