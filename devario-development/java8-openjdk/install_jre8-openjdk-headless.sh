THIS_JRE='java-8-openjdk/jre'

fix_default() {
  if [ ! -x /usr/bin/java ]; then
    /usr/bin/devario-java unset
    echo ""
  else
    /usr/bin/devario-java get
  fi
}

post_install() {
  default=$(fix_default)
  case ${default} in
    "")
      /usr/bin/devario-java set ${THIS_JRE}
      ;;
    ${THIS_JRE} | ${THIS_JRE/\/jre})
      # Nothing
      ;;
    *)
      echo "Default Java environment is already set to '${default}'"
      echo "See 'devario-java help' to change it"
      ;;
  esac

  if [ ! -f /etc/ssl/certs/java/cacerts ]; then
    /usr/bin/update-ca-trust
  fi
}

post_upgrade() {
  if [ -z $(fix_default) ]; then
    /usr/bin/devario-java set ${THIS_JRE}
  fi

  if [ ! -f /etc/ssl/certs/java/cacerts ]; then
    /usr/bin/update-ca-trust
  fi
}

pre_remove() {
  default=$(fix_default)
  if [ "x${default/\/jre}" = "x${THIS_JRE/\/jre}" ]; then
    /usr/bin/devario-java unset
    echo "No Java environment is set as default anymore"
  fi
}
