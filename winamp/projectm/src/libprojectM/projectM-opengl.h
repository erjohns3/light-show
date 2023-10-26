/**
   Include appropriate OpenGL headers for this platform.
**/

#ifndef  __PROJECTM_OPENGL_H__
#define  __PROJECTM_OPENGL_H__

// stuff that needs to be ported to newer GL calls
#define GL_TRANSITION

// Enable openGL extra checks, better not be enabled in release build
#define OGL_DEBUG                   0

// If a shader compilation failure occurs, it dumps shader source into /tmp instead of stderr
#define DUMP_SHADERS_ON_ERROR       0

# if USE_GLES
#  include <GLES3/gl3.h>
# else
#  if !defined(GL_GLEXT_PROTOTYPES)
#     define GL_GLEXT_PROTOTYPES
#  endif
#  include <GL/gl.h>
#  include <GL/glext.h>
# endif


#endif // __PROJECTM_OPENGL_H__
