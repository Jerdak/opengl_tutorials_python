from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *

#return GLuint
def LoadShaders(vertex_file_path,fragment_file_path):
	# Create the shaders
	VertexShaderID = glCreateShader(GL_VERTEX_SHADER)
	FragmentShaderID = glCreateShader(GL_FRAGMENT_SHADER)

	# Read the Vertex Shader code from the file
	VertexShaderCode = ""
	with open(vertex_file_path,'r') as fr:
		for line in fr:
			VertexShaderCode += line
		# alternatively you could use fr.readlines() and then join in to a single string 

	FragmentShaderCode = ""
	with open(fragment_file_path,'r') as fr:
		for line in fr:
			FragmentShaderCode += line
		# alternatively you could use fr.readlines() and then join in to a single string 

	# Compile Vertex Shader
	print("Compiling shader: %s"%(vertex_file_path))
	glShaderSource(VertexShaderID, VertexShaderCode)
	glCompileShader(VertexShaderID)

	# Check Vertex Shader
	result = glGetShaderiv(VertexShaderID, GL_COMPILE_STATUS)
	if not result:
		raise RuntimeError(glGetShaderInfoLog(VertexShaderID))

	# Compile Fragment Shader
	print("Compiling shader: %s"%(fragment_file_path))
	glShaderSource(FragmentShaderID,FragmentShaderCode)
	glCompileShader(FragmentShaderID)

	# Check Fragment Shader
	result = glGetShaderiv(VertexShaderID, GL_COMPILE_STATUS)
	if not result:
		raise RuntimeError(glGetShaderInfoLog(FragmentShaderID))



	# Link the program
	print("Linking program")
	ProgramID = glCreateProgram()
	glAttachShader(ProgramID, VertexShaderID)
	glAttachShader(ProgramID, FragmentShaderID)
	glLinkProgram(ProgramID)

	# Check the program
	result = glGetShaderiv(VertexShaderID, GL_COMPILE_STATUS)
	if not result:
		raise RuntimeError(glGetShaderInfoLog(ProgramID))

	glDeleteShader(VertexShaderID);
	glDeleteShader(FragmentShaderID);

	return ProgramID;
'''
WINDOW_SIZE = 640, 480
def init_glut(argv):
	"""glut initialization."""
	glutInit(argv)
	glutInitWindowSize(*WINDOW_SIZE)
	glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE|GLUT_DEPTH)
	
	glutCreateWindow(argv[0].encode())
	
	glutReshapeFunc(reshape)
	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard)
	glutMouseFunc(mouse)
	glutMotionFunc(motion)

def keyboard(c, x=0, y=0):
	"""keyboard callback."""
	global perspective, lighting, texturing
	
	if c == PERSPECTIVE:
		perspective = not perspective
		reshape(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
	
	elif c == LIGHTING:
		lighting = not lighting
		glUniform1i(locations[b"lighting"], lighting)
	
	elif c == TEXTURING:
		texturing = not texturing
		glUniform1i(locations[b"texturing"], texturing)
		if texturing:
			animate_texture()
	
	elif c == b's':
		screen_shot()
	
	elif c == b'q':
		sys.exit(0)
	glutPostRedisplay()	
def display():
	"""window redisplay callback."""
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	draw_object()
	glutSwapBuffers()

def reshape(width, height):
	"""window reshape callback."""
	glViewport(0, 0, width, height)
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	radius = .5 * min(width, height)
	w, h = width/radius, height/radius
	if perspective:
		glFrustum(-w, w, -h, h, 8, 16)
		glTranslate(0, 0, -12)
		glScale(1.5, 1.5, 1.5)
	else:
		glOrtho(-w, w, -h, h, -2, 2)
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
def init_opengl():
	# depth test
	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	
	# lighting
	light_position = [1., 1., 2., 0.]
	glLight(GL_LIGHT0, GL_POSITION, light_position)
	glMaterialfv(GL_FRONT, GL_SPECULAR, [1., 1., 1., 1.])
	glMaterialf(GL_FRONT, GL_SHININESS, 100.)	
	
	# initial state
	for k in [PERSPECTIVE, LIGHTING, TEXTURING]:
		keyboard(k)

def init_shaders():
	LoadShaders("SimpleVertexShader.vertexshader","SimpleFragmentShader.fragmentshader")

def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	init_glut(argv)
	init_shaders()
	init_opengl()
	return glutMainLoop()
	#LoadShaders("SimpleVertexShader.vertexshader","SimpleFragmentShader.fragmentshader")
if __name__ == "__main__":
	sys.exit(main())
'''