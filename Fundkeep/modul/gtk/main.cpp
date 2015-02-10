#include <gtk/gtk.h>

int main(int argc, char** argv)
{
	GtkWidget *label;
	GtkWidget *window;
	GtkWidget *frame;
	gtk_init(&argc, &argv);
	
	
	window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
	gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);
	gtk_window_set_default_size(GTK_WINDOW(window), 300, 180);
	gtk_window_set_title(GTK_WINDOW(window), "Fundkeep (c) Makin 2013");
	
	frame = gtk_fixed_new();
	gtk_container_add(GTK_CONTAINER(window), frame);
	
	
	label = gtk_label_new("argv[1]");
	gtk_fixed_put(GTK_FIXED(frame), label, 190, 58); 
	
	
	
	
	gtk_window_set_opacity(GTK_WINDOW(window), 0.8);
	
	
	gtk_widget_show_all(window);

	g_signal_connect(window, "destroy",G_CALLBACK (gtk_main_quit), NULL);

	//~ g_signal_connect(plus, "clicked", 
	  //~ G_CALLBACK(increase), label);
//~ 
	//~ g_signal_connect(minus, "clicked", 
	  //~ G_CALLBACK(decrease), label);

	gtk_main();
	return 0;

}
