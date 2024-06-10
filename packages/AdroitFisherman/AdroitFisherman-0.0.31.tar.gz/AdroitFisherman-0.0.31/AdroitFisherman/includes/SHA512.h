#ifndef SHA512_H
#define SHA512_H
uint64_t Rotr_64(uint64_t source, int value)
{
    return source >> value | (source << 64 - value);
}
typedef struct {
    PyObject_HEAD
    unsigned char* data;
    unsigned int* source_bytes;
    unsigned char* encrypted_data;
    uint64_t* packet_blocks;
    uint64_t* WHandler;
    uint64_t h0, h1, h2, h3, h4, h5, h6, h7, h8;
    uint64_t a, b, c, d, e, f, g, h;
}SHAblock;
static SHABlock_destroy(SHAblock*self)
{
    Py_TYPE(self)->tp_free(self);
}
static SHABlock_new(PyTypeObject*type,PyObject*args,PyObject*kwds)
{
    SHAblock* self=(SHAblock*)type->tp_alloc(type,0);
    if (self == NULL)
    {
        return NULL;
    }
    else
    {
        self->data = NULL;
        self->source_bytes = NULL;
        self->packet_blocks = NULL;
        self->WHandler = NULL;
        self->encrypted_data = NULL;
        Py_XINCREF(self);
        return (PyObject*)self;
    }
}
static int SHABlock_init(SHAblock*self,PyObject*args,PyObject*kwds)
{
    return 0;
}
static PyMemberDef SHABlock_members[] = {
    {NULL}
};
static PyObject* convert_SHA512(SHAblock*self,PyObject*args)
{
    unsigned char* msg;
    if (PyArg_ParseTuple(args,"y",&msg)<0)
    {
        Py_RETURN_NONE;
    }
    else
    {
        uint64_t sha_8_box[] = {
        0x6A09E667F3BCC908,//a=3   h00
        0xBB67AE8584CAA73B,//b=5   h01
        0x3C6EF372FE94F82B,//c=7   h02
        0xA54FF53A5F1D36F1,//d=11  h03
        0x510E527FADE682D1,//e=13  h04
        0x9B05688C2B3E6C1F,//f=17  h05
        0x1F83D9ABFB41BD6B,//g=19  h06
        0x5BE0CD19137E2179// h=23  h07
        };
        uint64_t sha_64_box[] = {
            0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
            0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
            0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
            0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
            0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
            0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
            0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
            0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
            0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
            0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
            0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
            0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
            0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
            0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
            0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
            0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
            0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
            0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
            0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
            0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
        };
        self->data = (unsigned char*)malloc(sizeof(unsigned char) * strlen(msg));
        int counter = 0;
        while (counter < strlen(msg))
        {
            self->data[counter] = msg[counter];
            counter++;
        }
        self->data[counter] = '\0';
        self->source_bytes = (unsigned int*)malloc(sizeof(unsigned int) * strlen(msg));
        for (int i = 0; i < strlen(msg); i++)
        {
            self->source_bytes[i] = 0;
        }
        counter = 0;
        for (int i = 0; i < strlen(msg); i++)
        {
            unsigned int bit_8 = self->data[i];
            self->source_bytes[counter++] = bit_8;
        }
        self->source_bytes[counter] = 0x1 << 7;
        int byte_length = counter * 8;
        int packets = byte_length / 1024;
        int paddings = byte_length % 1024;
        if (paddings > 0)
        {
            packets += 1;
        }
        self->packet_blocks = (uint64_t*)malloc(sizeof(uint64_t) * packets * 16);
        for (int i = 0; i < packets * 16; i++)
        {
            self->packet_blocks[i] = 0;
        }
        self->packet_blocks[(packets * 16) - 1] = byte_length;
        int counter1 = 0, counter2 = 0;
        while (counter1 <= counter)
        {
            uint64_t tmp = 0;
            tmp |= (uint64_t)self->source_bytes[counter1++] << 56;
            if (counter1 > counter)
            {
                self->packet_blocks[counter2++] = tmp;
                break;
            }
            tmp |= (uint64_t)self->source_bytes[counter1++] << 48;
            if (counter1 > counter)
            {
                self->packet_blocks[counter2++] = tmp;
                break;
            }
            tmp |= (uint64_t)self->source_bytes[counter1++] << 40;
            if (counter1 > counter)
            {
                self->packet_blocks[counter2++] = tmp;
                break;
            }
            tmp |= (uint64_t)self->source_bytes[counter1++] << 32;
            if (counter1 > counter)
            {
                self->packet_blocks[counter2++] = tmp;
                break;
            }
            tmp |= (uint64_t)self->source_bytes[counter1++] << 24;
            if (counter1 > counter)
            {
                self->packet_blocks[counter2++] = tmp;
                break;
            }
            tmp |= (uint64_t)self->source_bytes[counter1++] << 16;
            if (counter1 > counter)
            {
                self->packet_blocks[counter2++] = tmp;
                break;
            }
            tmp |= (uint64_t)self->source_bytes[counter1++] << 8;
            if (counter1 > counter)
            {
                self->packet_blocks[counter2++] = tmp;
                break;
            }
            tmp |= (uint64_t)self->source_bytes[counter1++];
            if (counter1 > counter)
            {
                self->packet_blocks[counter2++] = tmp;
                break;
            }
            self->packet_blocks[counter2++] = tmp;
        }
        self->h0 = sha_8_box[0];
        self->h1 = sha_8_box[1];
        self->h2 = sha_8_box[2];
        self->h3 = sha_8_box[3];
        self->h4 = sha_8_box[4];
        self->h5 = sha_8_box[5];
        self->h6 = sha_8_box[6];
        self->h7 = sha_8_box[7];
        self->WHandler = (uint64_t*)malloc(sizeof(uint64_t) * 80);
        for (int i = 0; i < packets; i++)
        {
            for (int j = 0; j < 16; j++)
            {
                self->WHandler[j] = self->packet_blocks[i * 16 + j];
            }
            for (int m = 16; m < 80; m++)
            {
                uint64_t w15 = self->WHandler[m - 15];
                uint64_t w2 = self->WHandler[m - 2];
                uint64_t w7 = self->WHandler[m - 7];
                uint64_t w16 = self->WHandler[m - 16];
                uint64_t w0 = (Rotr_64(w15, 1)) ^ (Rotr_64(w15, 8)) ^ ((w15 >> 7));
                uint64_t w1 = (Rotr_64(w2, 19)) ^ (Rotr_64(w2, 61)) ^ ((w2 >> 6));
                self->WHandler[m] = w1 + w7 + w0 + w16;

            }
            self->a = self->h0;
            self->b = self->h1;
            self->c = self->h2;
            self->d = self->h3;
            self->e = self->h4;
            self->f = self->h5;
            self->g = self->h6;
            self->h = self->h7;
            for (int k = 0; k < 80; k++)
            {
                uint64_t tmp_t1 = self->h + ((self->e & self->f) ^ ((~self->e) & self->g)) + (Rotr_64(self->e, 14) ^ Rotr_64(self->e, 18) ^ Rotr_64(self->e, 41)) + self->WHandler[k] + sha_64_box[k];
                uint64_t tmp_t2 = (Rotr_64(self->a, 28) ^ Rotr_64(self->a, 34) ^ Rotr_64(self->a, 39)) + ((self->a & self->b) ^ (self->a & self->c) ^ (self->b & self->c));
                self->h = self->g;
                self->g = self->f;
                self->f = self->e;
                self->e = self->d + tmp_t1;
                self->d = self->c;
                self->c = self->b;
                self->b = self->a;
                self->a = tmp_t1 + tmp_t2;
            }
            self->h0 += self->a;
            self->h1 += self->b;
            self->h2 += self->c;
            self->h3 += self->d;
            self->h4 += self->e;
            self->h5 += self->f;
            self->h6 += self->g;
            self->h7 += self->h;
        }
        self->encrypted_data = (unsigned char*)malloc(sizeof(unsigned char) * 512);
        sprintf(self->encrypted_data, "%016llx%016llx%016llx%016llx%016llx%016llx%016llx%016llx", self->h0, self->h1, self->h2, self->h3, self->h4, self->h5, self->h6, self->h7);
        PyObject* result = Py_BuildValue("y",self->encrypted_data);
        Py_INCREF(result);
        return result;
    }
}
static PyObject* destroy(SHAblock*self)
{
    free(self->encrypted_data);
    free(self->WHandler);
    free(self->data);
    free(self->source_bytes);
    free(self->packet_blocks);
    Py_RETURN_NONE;
}
static PyObject* get_msg(SHAblock*self)
{
    PyObject* result = Py_BuildValue("y",self->data);
    Py_INCREF(result);
    return result;
}
static PyMethodDef SHABlock_methods[] = {
    {"update",convert_SHA512,METH_VARARGS,""},
    {"destroy_sha512",destroy,METH_NOARGS,""},
    {"get_data",get_msg,METH_NOARGS,""},
    {NULL}
};
static PyTypeObject SHABlock_object = {
    PyVarObject_HEAD_INIT(NULL,0)
    .tp_name = "SHAUtility.SHABlock",
    .tp_new = SHABlock_new,
    .tp_dealloc = (destructor)SHABlock_destroy,
    .tp_init = (initproc)SHABlock_init,
    .tp_members = SHABlock_members,
    .tp_methods = SHABlock_methods,
    .tp_basicsize = sizeof(SHAblock),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_BASETYPE | Py_TPFLAGS_DEFAULT
};
#endif // !SHA512_H
