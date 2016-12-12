/**
 * @file common.c
 * @author Izzulmakin 2016-05-10
 * provide commonly used api
 */
 #include "common.h"


wchar_t debugstring[200];

/** my custom api in Django */
/** global pointer refer to value returned by cloud_data_read */
char * cloud_data_value;


/** read data in server */
char * cloud_data_read(char *name)
{
	free(cloud_data_value);
	char *cmd = malloc(sizeof(char) * (117+2*128));
	sprintf(cmd,
			"tools\\curl\\curl.exe http://makin.pythonanywhere.com/cloud_data/aaa/read/%s/",
			name
		);
	cloud_data_value = exec(cmd);
	free(cmd);
	return cloud_data_value;
}


/** write data in server */
void cloud_data_write(char *name, char *value)
{
	char *cmd = malloc(sizeof(char) * (117+2*128));
	sprintf(cmd,
			"tools\\curl\\curl.exe http://makin.pythonanywhere.com/cloud_data/aaa/write/%s/%s",
			name,
			value
		);
	printlog("\n");
	printlog("\n");
	printlog(cmd);
	exec(cmd);
	free(cmd);
}


void calibrate_window(int width, int height)
{
	char repeat = 1;
	while(repeat!=0)
	{
		//~ pixelsearch_nothread(icon_search, 0,0,1366,768, 
	}
}

uint8_t calibrate_window_test1(long color, long x, long y)
{
	//~ if (color = 0x
}

/**
 * push
 * @param self linkedlist pointer
 * @param new_data linkedlist pointer to new data to be pushed
 */
void linkedlist_push(linkedlist *self, linkedlist *new_data)
{
	linkedlist *p;
	p = self;
	while (p->next!=0)
		p=p->next;
	
	new_data->next = 0;
	new_data->prev = p;
	p->next = new_data;
}

/**
 * get tail
 * @param self linkedlist pointer
 */
linkedlist * linkedlist_tail(linkedlist *self)
{
	linkedlist *p;
	p = self;
	while (p->next!=0)
		p = p->next;
	if (p->prev!=0)
		p = p->prev;
	return p->next;
}


/**
 * execute program and get stdoutput. 
 * @param cmd cmd string to be executed in shell
 * @return result stdout char*, 
 * please free the return value manually when done using,
 * function always malloc return value each time called
 */
char* exec(char* cmd) {
	FILE* pipe = popen(cmd, "r");
	if (!pipe) return "ERROR";
	char buffer[128];
	char *result = malloc(
				1000* //possible max result size
				sizeof(char)			
			);
	result[0] = 0;//null for strcat will seek to where to append
	while(!feof(pipe)) {
		if(fgets(buffer, 128, pipe) != NULL)
		{
			strcat(result, buffer);
		}
	}
	pclose(pipe);
	return result;
}
