THIS_JDK='java-8-openjdk'

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
    "" | ${THIS_JDK}/jre)
      /usr/bin/devario-java set ${THIS_JDK}
      ;;
    ${THIS_JDK})
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
  default=$(fix_default)
  if [ -z "${default}" -o "x${default}" = "x${THIS_JDK}/jre" ]; then
    /usr/bin/devario-java set ${THIS_JDK}
  fi

  if [ ! -f /etc/ssl/certs/java/cacerts ]; then
    /usr/bin/update-ca-trust
  fi
}

pre_remove() {
  if [ "x$(fix_default)" = "x${THIS_JDK}" ]; then
    /usr/bin/devario-java unset
    if [ -x /usr/lib/jvm/${THIS_JDK}/jre/bin/java ]; then
      /usr/bin/devario-java set ${THIS_JDK}/jre
    fi
  fi
}
