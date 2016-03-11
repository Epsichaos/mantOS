; Auto-generated. Do not edit!


(cl:in-package manta-msg)


;//! \htmlinclude Imu2.msg.html

(cl:defclass <Imu2> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:float
    :initform 0.0))
)

(cl:defclass Imu2 (<Imu2>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Imu2>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Imu2)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name manta-msg:<Imu2> is deprecated: use manta-msg:Imu2 instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <Imu2>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader manta-msg:x-val is deprecated.  Use manta-msg:x instead.")
  (x m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Imu2>) ostream)
  "Serializes a message object of type '<Imu2>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Imu2>) istream)
  "Deserializes a message object of type '<Imu2>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Imu2>)))
  "Returns string type for a message object of type '<Imu2>"
  "manta/Imu2")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Imu2)))
  "Returns string type for a message object of type 'Imu2"
  "manta/Imu2")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Imu2>)))
  "Returns md5sum for a message object of type '<Imu2>"
  "abd5d1e9c3ac157a0df3ba27b65d3384")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Imu2)))
  "Returns md5sum for a message object of type 'Imu2"
  "abd5d1e9c3ac157a0df3ba27b65d3384")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Imu2>)))
  "Returns full string definition for message of type '<Imu2>"
  (cl:format cl:nil "float32 x~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Imu2)))
  "Returns full string definition for message of type 'Imu2"
  (cl:format cl:nil "float32 x~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Imu2>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Imu2>))
  "Converts a ROS message object to a list"
  (cl:list 'Imu2
    (cl:cons ':x (x msg))
))
